from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.behavior import BehaviorCreate
from app.services.behavior_service import BehaviorService
router=APIRouter(prefix="/behaviors",tags=["behaviors"])
@router.post("",status_code=201)
def record_behavior(payload:BehaviorCreate,db:Session=Depends(get_db)):
    if not BehaviorService(db).record(payload): raise HTTPException(404,"Product not found")
    return {"ok":True}
