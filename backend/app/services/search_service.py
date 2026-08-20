from app.repositories.product_repository import ProductRepository
class SearchService:
    def __init__(self, db): self.products = ProductRepository(db)
    def search(self, query, limit=20): return self.products.search(query.strip(), limit)
