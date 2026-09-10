from app.config import (
    BEHAVIOR_WEIGHTS,
    COLD_START_LEARNING_RATE,
    DETAIL_DWELL_FULL_SIGNAL_SECONDS,
    DETAIL_DWELL_MAX_WEIGHT,
    MATURE_PROFILE_LEARNING_RATE,
    PROFILE_MATURITY_LIKES,
)
from app.repositories.behavior_repository import BehaviorRepository
from app.repositories.user_repository import UserRepository

# 各维度一次行为的最大增量（写入偏好前统一裁剪到 [-1, 1]）。
MAX_WEIGHT = 1.0
MIN_WEIGHT = -1.0


class PreferenceService:
    def __init__(self, db):
        self.db = db
        self.users = UserRepository(db)
        self.behaviors = BehaviorRepository(db)

    def get(self, user_id):
        """获取（不存在则创建）指定用户的兴趣画像。"""
        return self.users.preference(user_id)

    def update_from_behavior(self, user_id, product, event_type, metadata=None):
        """根据一次行为更新兴趣画像。

        仅更新商品的 style_primary/style_secondary/category/color/fit 五个维度；
        事件权重来自 BEHAVIOR_WEIGHTS，归一化后累加到对应键并裁剪到 [-1, 1]。
        无权重事件（如 impression）保持画像不变。
        """
        if event_type == "detail_dwell":
            seconds = max(0, float((metadata or {}).get("duration_seconds", 0)))
            raw = min(DETAIL_DWELL_MAX_WEIGHT, seconds / DETAIL_DWELL_FULL_SIGNAL_SECONDS * DETAIL_DWELL_MAX_WEIGHT)
        else:
            raw = BEHAVIOR_WEIGHTS.get(event_type, 0)
        if not raw:
            return self.get(user_id)

        # 冷启动阶段将单次反馈均摊到 100 件喜欢商品中。这样首个喜欢只产生
        # +0.01 的偏好信号，不会让后续 Feed 被一种风格迅速占满。
        liked_count = self.behaviors.liked_product_count(user_id)
        learning_rate = (
            COLD_START_LEARNING_RATE
            if liked_count < PROFILE_MATURITY_LIKES
            else MATURE_PROFILE_LEARNING_RATE
        )
        delta = max(MIN_WEIGHT, min(MAX_WEIGHT, raw / 3.0)) * learning_rate
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
