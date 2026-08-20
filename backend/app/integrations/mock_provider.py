from app.integrations.base import ProductProvider
from app.repositories.product_repository import ProductRepository
class MockProductProvider(ProductProvider):
    def __init__(self, db): self.products=ProductRepository(db)
    def search_products(self, query): return self.products.search(query)
    def get_product(self, external_id): return self.products.get(int(external_id))
