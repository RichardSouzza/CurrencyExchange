import secrets
from datetime import datetime, timedelta
from os import getenv
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import Depends, Request
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery, HTTPBearer 
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from server.exceptions import InvalidTokenException
from server.models import TokenData


load_dotenv()

cookie_scheme = APIKeyCookie(name="session")
header_scheme = APIKeyHeader(name="Authorization")
query_scheme = APIKeyQuery(name="token")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True) -> None:
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise InvalidTokenException()
            if not verify_token(credentials.credentials):
                raise InvalidTokenException()
            return credentials
        else:
            raise InvalidTokenException()


def create_token(data: dict, token_expire_minutes: int = TOKEN_EXPIRE_MINUTES) -> str:
    to_encode_data = data.copy()
    expire = datetime.now() + timedelta(minutes=token_expire_minutes)
    to_encode_data.update({"expire_time": str(expire)})
    token = jwt.encode(to_encode_data, SECRET_KEY, ALGORITHM) # type: ignore
    return token


def get_payload(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        return payload
    except JWTError:
        return None


def get_active_token(token: Annotated[str, Depends(header_scheme)]) -> TokenData:
    if verify_token(token):
        payload = get_payload(token) or dict()
        token_type = payload.get("type")
        if token_type:
            return TokenData(type=token_type)
    raise InvalidTokenException()


def verify_token(token: str) -> bool:
    payload = get_payload(token)
    if payload:
        expire_time = payload.get("expire_time")
        if expire_time:
            expire_time = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S.%f")
            if datetime.now() < expire_time:
                return True
    return False


def generate_secret_key() -> str:
    return secrets.token_hex(32)
