from sqlalchemy import delete, distinct, func, select
from sqlalchemy.orm import Session
from app.models.behavior import UserBehavior
from app.models.product import Product

class BehaviorRepository:
    def __init__(self, db: Session): self.db = db
    def create(self, **data) -> UserBehavior:
        record = UserBehavior(**data); self.db.add(record); self.db.flush(); return record
    def liked_products(self, user_id: str) -> list[Product]:
        records = self.db.query(UserBehavior).filter_by(user_id=user_id, event_type="like").order_by(UserBehavior.created_at.desc()).all()
        seen: set[int] = set(); products: list[Product] = []
        for record in records:
            if record.product_id not in seen:
                product = self.db.get(Product, record.product_id)
                if product: products.append(product)
                seen.add(record.product_id)
        return products

    def liked_product_count(self, user_id: str) -> int:
        """返回用户喜欢过的不同商品数，重复点击不加速画像成熟。"""
        stmt = select(func.count(distinct(UserBehavior.product_id))).where(
            UserBehavior.user_id == user_id,
            UserBehavior.event_type == "like",
        )
        return int(self.db.scalar(stmt) or 0)

    def has_liked_product(self, user_id: str, product_id: int) -> bool:
        return self.db.scalar(
            select(UserBehavior.id).where(
                UserBehavior.user_id == user_id,
                UserBehavior.product_id == product_id,
                UserBehavior.event_type == "like",
            ).limit(1)
        ) is not None

    def delete_likes(self, user_id: str, product_id: int) -> int:
        result = self.db.execute(
            delete(UserBehavior).where(
                UserBehavior.user_id == user_id,
                UserBehavior.product_id == product_id,
                UserBehavior.event_type == "like",
            )
        )
        return int(result.rowcount or 0)
