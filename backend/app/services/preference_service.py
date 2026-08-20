from app.config import BEHAVIOR_WEIGHTS
from app.repositories.user_repository import UserRepository

# 各维度一次行为的最大增量（写入偏好前统一裁剪到 [-1, 1]）。
MAX_WEIGHT = 1.0
MIN_WEIGHT = -1.0


class PreferenceService:
    def __init__(self, db):
        self.db = db
        self.users = UserRepository(db)

    def get(self, user_id):
        """获取（不存在则创建）指定用户的兴趣画像。"""
        return self.users.preference(user_id)

    def update_from_behavior(self, user_id, product, event_type):
        """根据一次行为更新兴趣画像。

        仅更新商品的 style_primary/style_secondary/category/color/fit 五个维度；
        事件权重来自 BEHAVIOR_WEIGHTS，归一化后累加到对应键并裁剪到 [-1, 1]。
        无权重事件（如 impression）保持画像不变。
        """
        raw = BEHAVIOR_WEIGHTS.get(event_type, 0)
        if not raw:
            return self.get(user_id)

        # 原始权重如 +3/-3 直接累加会一步封顶，除以 3 得到约 [-1, 1] 的单步增量。
        delta = max(MIN_WEIGHT, min(MAX_WEIGHT, raw / 3.0))
        pref = self.get(user_id)

        updates = {
            "styles": [(product.style_primary, 1.0), (product.style_secondary, 0.5)],
            "categories": [(product.category, 1.0)],
            "colors": [(product.color, 1.0)],
            "fits": [(product.fit, 1.0)],
        }
        for field, entries in updates.items():
            values = dict(getattr(pref, field) or {})
            for key, factor in entries:
                if not key:
                    continue
                values[key] = max(MIN_WEIGHT, min(MAX_WEIGHT, values.get(key, 0.0) + delta * factor))
            setattr(pref, field, values)

        self.db.flush()
        return pref
