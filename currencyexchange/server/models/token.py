from enum import Enum

from pydantic import BaseModel


class TokenType(str, Enum):
    read = "read"
    write = "write"


class TokenData(BaseModel):
    type: TokenType
