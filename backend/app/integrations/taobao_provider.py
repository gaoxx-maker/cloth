from app.integrations.base import ProductProvider
class TaobaoProvider(ProductProvider):
    """TODO: map Taobao API responses to the normalized Product contract; do not leak vendor fields."""
    def search_products(self, query): raise NotImplementedError("Requires an approved Taobao API integration")
    def get_product(self, external_id): raise NotImplementedError("Requires an approved Taobao API integration")
