from pydantic import BaseModel, Field


class Currency(BaseModel):
    code: str
    name: str
    decimals: int
    # rates: dict[str, int]
    # history: dict[str, rates]
    
    class Config:
        frozen = True


class SetCurrency(BaseModel):
    id: int
    code: str = Field(max_length=3)
    name: str
    decimals: int
    # rates: dict[str, int]
    # history: dict[str, rates]
    
    class Config:
        frozen = True
