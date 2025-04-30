from pydantic import BaseModel


class TokenData(BaseModel):
    type: str
