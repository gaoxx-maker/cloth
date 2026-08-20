from sqlalchemy.orm import Session
from app.models.behavior import UserBehavior

class BehaviorRepository:
    def __init__(self, db: Session): self.db = db
    def create(self, **data) -> UserBehavior:
        record = UserBehavior(**data); self.db.add(record); self.db.flush(); return record
