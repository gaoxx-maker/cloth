from collections.abc import Generator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.account import Account
from app.repositories.account_repository import AccountRepository
from app.security import TokenError, decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_optional_current_account(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme), db: Session = Depends(get_db)) -> Account | None:
    if not credentials: return None
    try: payload = decode_access_token(credentials.credentials)
    except TokenError as exc: raise HTTPException(401, "登录状态无效或已过期") from exc
    account = AccountRepository(db).get(payload["sub"])
    if not account or not account.is_active: raise HTTPException(401, "登录状态无效或账户已停用")
    return account

def get_current_account(account: Account | None = Depends(get_optional_current_account)) -> Account:
    if not account: raise HTTPException(401, "请先登录")
    return account

def require_admin(account: Account = Depends(get_current_account)) -> Account:
    if account.role != "admin": raise HTTPException(403, "需要管理员权限")
    return account
