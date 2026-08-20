from app.repositories.product_repository import ProductRepository
class ProductService:
    def __init__(self, db): self.products = ProductRepository(db)
    def get_product(self, product_id): return self.products.get(product_id)
    def list_products(self, limit=20, offset=0): return self.products.list_products(limit, offset)
