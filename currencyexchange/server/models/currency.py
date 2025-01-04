from pydantic import BaseModel


class Currency(BaseModel):
    code: str
    name: str
    decimals: int
    # rates: dict[str, int]
    # history: dict[str, rates]
    
    class Config:
        frozen = True
