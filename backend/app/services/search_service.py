from app.repositories.product_repository import ProductRepository
from app.config import get_settings
from app.integrations.jd_provider import JDProvider, get_jd_provider


class SearchService:
    def __init__(self, db, jd_provider: JDProvider | None = None):
        self.products = ProductRepository(db)
        self.jd_provider = jd_provider or get_jd_provider()

    def search(self, query, limit=20):
        """Return virtual-library results first; JD may add only a tiny tail."""
        query = query.strip()
        remote_limit = min(get_settings().jd_max_products_per_search, max(0, limit - 1))
        local = self.products.search(query, limit)
        if remote_limit == 0:
            return local[:limit]
        remote = self.jd_provider.search_products(query)[:remote_limit]
        return [*local[: limit - len(remote)], *remote]
