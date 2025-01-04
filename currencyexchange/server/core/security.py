import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from dotenv import dotenv_values
from jose import JWTError, jwt


settings = dotenv_values()

SECRET_KEY = settings.get("SECRET_KEY") or ""
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict) -> str:
    to_encode_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode_data.update({"expire_time": expire})
    token_jwt = jwt.encode(to_encode_data, SECRET_KEY, ALGORITHM)
    return token_jwt


def check_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_secret_key() -> str:
    return secrets.token_hex(32)
