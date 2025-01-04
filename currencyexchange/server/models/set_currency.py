from pydantic import BaseModel, Field
from typing import Optional


class SetCurrency(BaseModel):
    id: int
    code: str = Field(max_length=3)
    name: str
    decimals: int
    # rates: dict[str, int]
    # history: dict[str, rates]
    
    class Config:
        frozen = True
