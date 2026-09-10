from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_account, get_db
from app.models.account import Account
from app.schemas.behavior import BehaviorCreate
from app.services.behavior_service import BehaviorService
router=APIRouter(prefix="/behaviors",tags=["behaviors"])
@router.post("",status_code=201)
def record_behavior(payload:BehaviorCreate,account:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    if not BehaviorService(db).record(account.id,payload): raise HTTPException(404,"Product not found")
    return {"ok":True}

@router.delete("/likes/{product_id}")
def remove_like(product_id:int,account:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    if not BehaviorService(db).remove_like(account.id,product_id): raise HTTPException(404,"Product not found")
    return {"ok":True}
