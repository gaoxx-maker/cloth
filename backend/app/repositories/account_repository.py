from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.account import Account


class AccountRepository:
    def __init__(self, db: Session): self.db = db
    def get(self, account_id: str) -> Account | None: return self.db.get(Account, account_id)
    def get_by_email(self, email: str) -> Account | None: return self.db.query(Account).filter_by(email=email).one_or_none()
    def create(self, **data) -> Account:
        account = Account(**data); self.db.add(account); self.db.flush(); return account
    def touch_login(self, account: Account) -> None:
        account.last_login_at = datetime.now(timezone.utc); self.db.flush()
    def list(self, offset: int = 0, limit: int = 50) -> list[Account]:
        return self.db.query(Account).order_by(Account.created_at.desc()).offset(offset).limit(limit).all()
