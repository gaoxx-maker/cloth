import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_settings
from app.dependencies import get_current_account, get_db
from app.models.account import Account
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AccountRead, LoginRequest, RegisterRequest, TokenResponse
from app.security import TokenError, create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
def token_response(account: Account) -> dict:
    try: token, expires_at = create_access_token(account.id, account.role)
    except TokenError as exc: raise HTTPException(503, str(exc)) from exc
    return {"access_token": token, "expires_at": expires_at, "user": account}

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    accounts = AccountRepository(db)
    if accounts.get_by_email(payload.email): raise HTTPException(409, "该邮箱已注册，请直接登录")
    settings = get_settings()
    is_admin = bool(settings.bootstrap_admin_email and settings.bootstrap_admin_code and payload.email == settings.bootstrap_admin_email.strip().lower() and payload.bootstrap_admin_code == settings.bootstrap_admin_code)
    account = accounts.create(id=str(uuid.uuid4()), email=payload.email, display_name=payload.display_name.strip(), password_hash=hash_password(payload.password), role="admin" if is_admin else "user")
    UserRepository(db).ensure_registered_user(account.id)
    db.commit()
    return token_response(account)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    account = AccountRepository(db).get_by_email(payload.email.strip().lower())
    if not account or not verify_password(payload.password, account.password_hash): raise HTTPException(401, "邮箱或密码不正确")
    if not account.is_active: raise HTTPException(403, "该账户已停用")
    AccountRepository(db).touch_login(account); UserRepository(db).ensure_registered_user(account.id); db.commit()
    return token_response(account)

@router.get("/me", response_model=AccountRead)
def me(account: Account = Depends(get_current_account)): return account
