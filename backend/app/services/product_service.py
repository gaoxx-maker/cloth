from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductRead


class ProductService:
    def __init__(self, db): self.products = ProductRepository(db)
    def get_product(self, product_id): return self.products.get(product_id)
    def list_products(self, limit=20, offset=0): return self.products.list_products(limit, offset)

    def similar_products(self, product_id, limit=6):
        return self.products.search_similar(product_id, limit)

    def get_product_detail(self, product_id):
        product = self.products.get(product_id)
        if not product: return None
        detail = ProductRead.model_validate(product).model_dump()
        detail["offers"] = [{"id": offer.id, "platform": platform.name if platform else "模拟商户", "platform_code": platform.code if platform else "unknown", "price": offer.price, "original_price": offer.original_price, "product_url": offer.product_url} for offer, platform in self.products.offers_for(product)]
        return detail

    def get_merchant_product(self, platform_code, catalog_id): return self.products.merchant_product(platform_code, catalog_id)
