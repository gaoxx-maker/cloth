from pydantic import BaseModel, Field

class BehaviorCreate(BaseModel):
    user_id: str; product_id: int; event_type: str
    session_id: str | None = None
    metadata: dict = Field(default_factory=dict)
