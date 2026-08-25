from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_account, get_db
from app.models.account import Account
from app.repositories.behavior_repository import BehaviorRepository
from app.schemas.product import ProductRead
from app.schemas.user import UserPreferenceRead
from app.services.preference_service import PreferenceService
router=APIRouter(prefix="/users",tags=["users"])
@router.get("/me/preferences",response_model=UserPreferenceRead)
def preferences(account:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    pref=PreferenceService(db).get(account.id); db.commit(); return {"user_id":account.id,**{key:getattr(pref,key) for key in ["styles","categories","colors","fits","price_min","price_max"]}}

@router.get("/me/likes", response_model=list[ProductRead])
def likes(account:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    return BehaviorRepository(db).liked_products(account.id)
