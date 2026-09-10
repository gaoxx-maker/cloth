from pydantic import BaseModel, Field

class BehaviorCreate(BaseModel):
    product_id: int; event_type: str
    session_id: str | None = None
    metadata: dict = Field(default_factory=dict)
