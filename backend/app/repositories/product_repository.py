from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.platform import Platform
from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def list_products(self, limit: int = 20, offset: int = 0) -> list[Product]:
        primary = list(self.db.scalars(select(Product).where(Product.external_product_id.like("%:jd")).offset(offset).limit(limit)))
        return primary or list(self.db.scalars(select(Product).offset(offset).limit(limit)))

    def candidates(self, limit: int = 1000) -> list[Product]:
        """随机抽取一批候选商品用于推荐打分。

        不读取全部 5000 件商品，而是随机抽样，避免每批 Feed 反复出现同一批商品。
        需要可复现实验时，可将随机抽样替换为按 (user_id, session_id) 做种子的确定性抽样。
        """
        primary = list(self.db.scalars(select(Product).where(Product.external_product_id.like("%:jd")).order_by(func.random()).limit(limit)))
        return primary or list(self.db.scalars(select(Product).order_by(func.random()).limit(limit)))

    def search(self, query: str, limit: int = 20) -> list[Product]:
        """基于 ILIKE 的轻量文本搜索，覆盖 title/brand/category/color/style/description。

        后续可替换为 PostgreSQL 全文检索或 Elasticsearch，接口保持不变。
        """
        needle = f"%{query}%"
        stmt = (
            select(Product)
            .where(
                or_(
                    Product.title.ilike(needle),
                    Product.brand.ilike(needle),
                    Product.category.ilike(needle),
                    Product.color.ilike(needle),
                    Product.style_primary.ilike(needle),
                    Product.style_secondary.ilike(needle),
                    Product.description.ilike(needle),
                )
            )
            .limit(limit)
        )
        primary = list(self.db.scalars(stmt.where(Product.external_product_id.like("%:jd"))))
        return primary or list(self.db.scalars(stmt))

    @staticmethod
    def catalog_id(product: Product) -> str | None:
        if not product.external_product_id or ":" not in product.external_product_id:
            return None
        return product.external_product_id.rsplit(":", 1)[0]

    def offers_for(self, product: Product) -> list[tuple[Product, Platform | None]]:
        catalog_id = self.catalog_id(product)
        if not catalog_id:
            return []
        stmt = select(Product, Platform).outerjoin(Platform, Product.platform_id == Platform.id).where(Product.external_product_id.like(f"{catalog_id}:%")).order_by(Product.price)
        return list(self.db.execute(stmt).all())

    def merchant_product(self, platform_code: str, catalog_id: str) -> Product | None:
        stmt = select(Product).join(Platform, Product.platform_id == Platform.id).where(Platform.code == platform_code, Product.external_product_id == f"{catalog_id}:{platform_code}")
        return self.db.scalar(stmt)

    def search_similar(self, product_id: int, limit: int = 20) -> list[Product]:
        """按属性相似度返回与指定商品相似的商品（排除自身）。

        第一版用共享属性数量（主风格 > 类目 > 颜色）做启发式排序；
        后续可替换为 pgvector 或独立向量服务，契约不变。
        """
        product = self.get(product_id)
        if not product:
            return []
        candidates = [p for p in self.candidates(limit=500) if p.id != product_id]

        def overlap(p: Product) -> int:
            score = 0
            if p.style_primary == product.style_primary:
                score += 3
            if p.category == product.category:
                score += 2
            if p.color == product.color:
                score += 1
            return score

        return sorted(candidates, key=overlap, reverse=True)[:limit]
