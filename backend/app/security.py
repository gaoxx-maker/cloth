"""Dependency-free password and HS256 JWT helpers."""
import base64, hashlib, hmac, json, secrets, time
from app.config import get_settings

class TokenError(ValueError): pass
def _enc(value: bytes) -> str: return base64.urlsafe_b64encode(value).rstrip(b"=").decode()
def _dec(value: str) -> bytes: return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    return f"scrypt${_enc(salt)}${_enc(hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1))}"
def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, salt, expected = encoded.split("$", 2)
        actual = hashlib.scrypt(password.encode(), salt=_dec(salt), n=16384, r=8, p=1)
        return scheme == "scrypt" and hmac.compare_digest(actual, _dec(expected))
    except (ValueError, TypeError): return False
def _secret() -> bytes:
    settings = get_settings()
    if settings.environment.lower() == "production" and settings.auth_secret_key == "development-only-change-me":
        raise TokenError("AUTH_SECRET_KEY is not configured")
    return settings.auth_secret_key.encode()
def create_access_token(account_id: str, role: str) -> tuple[str, int]:
    expires_at = int(time.time()) + get_settings().auth_access_token_minutes * 60
    header = _enc(b'{"alg":"HS256","typ":"JWT"}')
    payload = _enc(json.dumps({"sub": account_id, "role": role, "exp": expires_at}, separators=(",", ":")).encode())
    signature = _enc(hmac.new(_secret(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{signature}", expires_at
def decode_access_token(token: str) -> dict:
    try:
        header, payload, signature = token.split(".")
        expected = _enc(hmac.new(_secret(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(signature, expected): raise TokenError("Invalid token")
        data = json.loads(_dec(payload))
        if not isinstance(data.get("sub"), str) or int(data.get("exp", 0)) <= time.time(): raise TokenError("Expired token")
        return data
    except TokenError: raise
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc: raise TokenError("Invalid token") from exc
