from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_optional_current_account
from app.models.account import Account
from app.schemas.recommendation import FeedResponse, RecommendedProduct, ReplaceRequest
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/feed", response_model=FeedResponse)
def feed(
    user_id: str | None = None,
    limit: int = 20,
    mode: str = Query("balanced", pattern="^(traditional|balanced|explore)$"),
    session_id: str | None = None,
    account: Account | None = Depends(get_optional_current_account),
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)
    resolved_user_id = account.id if account else user_id
    if not resolved_user_id: raise HTTPException(400, "user_id is required for anonymous visitors")
    result = service.feed(resolved_user_id, 50, min(limit, 50), mode, session_id)
    return {
        "items": result["items"],
        "meta": {
            "exploration_level": result["level"],
            "algorithm": "rule_v1",
            "mode": mode,
            "season": result["season"],
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
