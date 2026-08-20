from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user import UserPreferenceRead
from app.services.preference_service import PreferenceService
router=APIRouter(prefix="/users",tags=["users"])
@router.get("/{user_id}/preferences",response_model=UserPreferenceRead)
def preferences(user_id:str,db:Session=Depends(get_db)):
    pref=PreferenceService(db).get(user_id); db.commit(); return {"user_id":user_id,**{key:getattr(pref,key) for key in ["styles","categories","colors","fits","price_min","price_max"]}}
