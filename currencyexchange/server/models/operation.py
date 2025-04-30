from pydantic import BaseModel


class OperationResult(BaseModel):
    success: bool
    data: object = None
    message: str = ""
