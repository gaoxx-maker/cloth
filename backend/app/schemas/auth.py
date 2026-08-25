from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)
    bootstrap_admin_code: str | None = None
    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"): raise ValueError("请输入有效邮箱")
        return value

class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=128)

class AccountRead(BaseModel):
    id: str; email: str; display_name: str; role: str; is_active: bool
    created_at: datetime | None = None

class TokenResponse(BaseModel):
    access_token: str; token_type: str = "bearer"; expires_at: int; user: AccountRead
