import secrets
from datetime import datetime, timedelta
from os import getenv
from typing import Any

from dotenv import load_dotenv
from fastapi import Request
from fastapi.security import APIKeyCookie, APIKeyHeader, APIKeyQuery, HTTPBearer 
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import JWTError, jwt

from server.exceptions import InvalidTokenException



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
            if not self.verify_token(credentials.credentials):
                raise InvalidTokenException()
            return credentials
        else:
            raise InvalidTokenException()

    def verify_token(self, token: str) -> bool:
        payload = get_playload(token)
        return True if payload else False


async def create_token(data: dict) -> str:
    to_encode_data = data.copy()
    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode_data.update({"expire_time": str(expire)})
    token = jwt.encode(to_encode_data, SECRET_KEY, ALGORITHM) # type: ignore
    return token


async def get_playload(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        return payload
    except JWTError:
        return None


async def generate_secret_key() -> str:
    return secrets.token_hex(32)


if __name__ == "__main__":
    data = {"type": "write"}
    print(create_token(data))
    ...