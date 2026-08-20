from pydantic import BaseModel
class UserPreferenceRead(BaseModel):
    user_id: str; styles: dict; categories: dict; colors: dict; fits: dict
    price_min: float | None = None; price_max: float | None = None
