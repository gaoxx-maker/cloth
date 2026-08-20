from abc import ABC, abstractmethod
class RecommendationEngine(ABC):
    @abstractmethod
    def recommend(self, user_id: str, candidates: list, exploration_level: int, limit: int) -> list:
        """Return scored product candidates. Must stay independent of FastAPI and SQLAlchemy."""
