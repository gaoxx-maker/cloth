from pydantic import BaseModel, Field

from app.schemas.product import ProductRead


class RecommendationInfo(BaseModel):
    score: float
    interest_score: float
    novelty_score: float
    reason: list[str]


class RecommendedProduct(ProductRead):
    recommendation: RecommendationInfo


class FeedResponse(BaseModel):
    items: list[RecommendedProduct]
    meta: dict


class ReplaceRequest(BaseModel):
    user_id: str
    product_id: int
    direction: str = Field(pattern="^(similar|explore|different)$")
    exploration_level: int = Field(default=50, ge=0, le=100)
    session_id: str | None = None
