from abc import ABC, abstractmethod
class ProductProvider(ABC):
    @abstractmethod
    def search_products(self, query: str): """Return normalized product results."""
    @abstractmethod
    def get_product(self, external_id: str): """Return one normalized product."""
