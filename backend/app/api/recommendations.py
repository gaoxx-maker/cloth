from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.recommendation import FeedResponse, RecommendedProduct, ReplaceRequest
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/feed", response_model=FeedResponse)
def feed(
    user_id: str,
    exploration_level: int = 50,
    limit: int = 20,
    mode: str = Query("balanced", pattern="^(baseline|balanced|explore)$"),
    session_id: str | None = None,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)
    result = service.feed(user_id, max(0, min(100, exploration_level)), min(limit, 50), mode, session_id)
    return {
        "items": result["items"],
        "meta": {
            "exploration_level": result["level"],
            "algorithm": "rule_v1",
            "mode": mode,
        },
    }


@router.post("/replace", response_model=RecommendedProduct)
def replace(payload: ReplaceRequest, db: Session = Depends(get_db)):
    result = RecommendationService(db).replace(
        payload.user_id,
        payload.product_id,
        payload.direction,
        payload.exploration_level,
        payload.session_id,
    )
    if not result:
        raise HTTPException(404, "No replacement found")
    return result
