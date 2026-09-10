from app.repositories.behavior_repository import BehaviorRepository
from app.services.preference_service import PreferenceService
from app.repositories.product_repository import ProductRepository
class BehaviorService:
    def __init__(self, db): self.db=db; self.behaviors=BehaviorRepository(db); self.products=ProductRepository(db); self.preferences=PreferenceService(db)
    def record(self, user_id: str, payload):
        product=self.products.get(payload.product_id)
        if not product: return None
        # 行为日志保留，但重复喜欢同一商品不能重复强化画像。
        is_repeat_like = payload.event_type == "like" and self.behaviors.has_liked_product(user_id, payload.product_id)
        record=self.behaviors.create(user_id=user_id, product_id=payload.product_id, event_type=payload.event_type, session_id=payload.session_id, metadata_=payload.metadata)
        if not is_repeat_like:
            self.preferences.update_from_behavior(user_id, product, payload.event_type, payload.metadata)
        self.db.commit(); return record

    def remove_like(self, user_id: str, product_id: int):
        product = self.products.get(product_id)
        if not product:
            return None
        if self.behaviors.delete_likes(user_id, product_id):
            # 喜欢记录已删除，反向写入同等强度的信号以撤销该次喜欢对画像的影响。
            self.preferences.update_from_behavior(user_id, product, "unlike")
        self.db.commit()
        return True
