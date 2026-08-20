from app.repositories.behavior_repository import BehaviorRepository
from app.services.preference_service import PreferenceService
from app.repositories.product_repository import ProductRepository
class BehaviorService:
    def __init__(self, db): self.db=db; self.behaviors=BehaviorRepository(db); self.products=ProductRepository(db); self.preferences=PreferenceService(db)
    def record(self, payload):
        product=self.products.get(payload.product_id)
        if not product: return None
        record=self.behaviors.create(user_id=payload.user_id, product_id=payload.product_id, event_type=payload.event_type, session_id=payload.session_id, metadata_=payload.metadata)
        self.preferences.update_from_behavior(payload.user_id, product, payload.event_type); self.db.commit(); return record
