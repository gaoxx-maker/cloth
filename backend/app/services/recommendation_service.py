from datetime import datetime

from app.config import STYLE_ADJACENCY
from app.models.recommendation import RecommendationLog
from app.recommendation.engine import RuleRecommendationEngine
from app.recommendation.explorer import reasons
from app.repositories.behavior_repository import BehaviorRepository
from app.repositories.product_repository import ProductRepository
from app.services.preference_service import PreferenceService

# 首页只保留三档模式，不再暴露“精准—探索”的连续调节。
MODE_TO_LEVEL = {"traditional": 25, "balanced": 50, "explore": 85}


def current_season(now: datetime | None = None) -> str:
    """按照服务器系统时间确定季节；北半球 3–5 春、6–8 夏、9–11 秋、12–2 冬。"""
    month = (now or datetime.now()).month
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    if month in (9, 10, 11):
        return "Autumn"
    return "Winter"


class RecommendationService:
    def __init__(self, db):
        self.db = db
        self.products = ProductRepository(db)
        self.behaviors = BehaviorRepository(db)
        self.preferences = PreferenceService(db)

    @staticmethod
    def _serialize(product, score, exploration_level, current_season, preference):
        """把 Product + 分数转换为与前端 RecommendedProduct 一致的字典，避免把 ORM 内部字段泄露到 API。"""
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "brand": product.brand,
            "category": product.category,
            "price": product.price,
            "color": product.color,
            "fit": product.fit,
            "style_primary": product.style_primary,
            "style_secondary": product.style_secondary,
            "style_tags": product.style_tags or [],
            "novelty_score": product.novelty_score,
            "quality_score": product.quality_score,
            "image_url": product.image_url,
            "recommendation": {
                "score": score["score"],
                "interest_score": score["interest_score"],
                "novelty_score": score["novelty_score"],
                "reason": reasons(product, score["interest_score"], exploration_level, current_season, preference),
            },
        }

    def _rank(self, user_id, candidates, exploration_level, limit, season=None):
        pref = self.preferences.get(user_id)
        season = season or current_season()
        rows = RuleRecommendationEngine(pref).recommend(user_id, candidates, exploration_level, limit, season)
        return [self._serialize(p, s, exploration_level, season, pref) for p, s in rows]

    def _record_behavior(self, user_id, product, event_type, session_id=None, metadata=None):
        """记录行为并同步更新兴趣画像。"""
        self.behaviors.create(
            user_id=user_id,
            product_id=product.id,
            event_type=event_type,
            session_id=session_id,
            metadata_=metadata or {},
        )
        self.preferences.update_from_behavior(user_id, product, event_type)

    def feed(self, user_id, exploration_level, limit, mode="balanced", session_id=None):
        """返回一页推荐，并写入推荐日志 + 首屏 impression 行为。"""
        level = MODE_TO_LEVEL[mode]

        season = current_season()
        items = self._rank(user_id, self.products.candidates(), level, limit, season)

        # 推荐日志：用于实验统计（探索度调节率、模式对比）。
        self.db.add(
            RecommendationLog(
                user_id=user_id,
                session_id=session_id,
                mode=mode,
                exploration_level=level,
                product_ids=[i["id"] for i in items],
            )
        )
        # 首屏 impression：作为 like_rate 等指标的分母。
        for item in items:
            self.behaviors.create(
                user_id=user_id,
                product_id=item["id"],
                event_type="impression",
                session_id=session_id,
                metadata_={"mode": mode, "exploration_level": level},
            )
        self.db.commit()
        return {"items": items, "level": level, "season": season}

    def replace(self, user_id, product_id, direction, exploration_level, session_id=None):
        """按方向返回一件替换商品，并记录一次 replace 行为。

        similar   ：同主风格、排除当前商品。
        explore   ：从相邻风格（见 STYLE_ADJACENCY）中选较高 novelty，探索度抬升。
        different ：排除当前主风格，仍以兴趣分作为最低门槛，保留一定相关概率。
        """
        product = self.products.get(product_id)
        if not product:
            return None

        candidates = [p for p in self.products.candidates() if p.id != product_id]
        level = exploration_level

        if direction == "similar":
            candidates = [p for p in candidates if p.style_primary == product.style_primary]
        elif direction == "explore":
            adjacent = STYLE_ADJACENCY.get(product.style_primary, [])
            narrowed = [p for p in candidates if p.style_primary in adjacent]
            candidates = narrowed or candidates
            level = max(exploration_level, 80)
        else:  # different
            candidates = [p for p in candidates if p.style_primary != product.style_primary]

        items = self._rank(user_id, candidates, level, 1)
        if not items:
            return None

        self._record_behavior(user_id, product, "replace", session_id, {"direction": direction})
        self.db.commit()
        return items[0]
