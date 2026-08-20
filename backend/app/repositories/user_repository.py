from sqlalchemy.orm import Session
from app.models.user import User, UserPreference

class UserRepository:
    def __init__(self, db: Session): self.db = db
    def ensure_user(self, user_id: str) -> User:
        user = self.db.get(User, user_id)
        if not user:
            user = User(id=user_id); self.db.add(user); self.db.flush()
        return user
    def preference(self, user_id: str) -> UserPreference:
        self.ensure_user(user_id)
        pref = self.db.query(UserPreference).filter_by(user_id=user_id).one_or_none()
        if not pref:
            pref = UserPreference(user_id=user_id); self.db.add(pref); self.db.flush()
        return pref
