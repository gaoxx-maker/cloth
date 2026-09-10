from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_admin
from app.models.account import Account
from app.repositories.account_repository import AccountRepository
from app.schemas.auth import AccountRead

router = APIRouter(prefix="/admin", tags=["admin"])
class AccountStatusUpdate(BaseModel): is_active: bool
@router.get("/users", response_model=list[AccountRead])
def list_users(_: Account = Depends(require_admin), db: Session = Depends(get_db)): return AccountRepository(db).list()
@router.patch("/users/{account_id}", response_model=AccountRead)
def update_user(account_id: str, payload: AccountStatusUpdate, _: Account = Depends(require_admin), db: Session = Depends(get_db)):
    account = AccountRepository(db).get(account_id)
    if not account: raise HTTPException(404, "用户不存在")
    account.is_active = payload.is_active; db.commit(); return account
