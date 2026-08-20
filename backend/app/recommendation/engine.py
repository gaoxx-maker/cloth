from app.recommendation.base import RecommendationEngine
from app.recommendation.scorer import score_product
from app.recommendation.diversity import rerank_diverse

class RuleRecommendationEngine(RecommendationEngine):
    def __init__(self, preference): self.preference = preference
    def recommend(self, user_id, candidates, exploration_level, limit):
        scored=[(product, score_product(self.preference, product, exploration_level)) for product in candidates]
        return rerank_diverse(scored, limit)
