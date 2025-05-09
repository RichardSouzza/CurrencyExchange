import logging

from fastapi import APIRouter

from server.infrastructure.security import create_token, verify_token as _verify_token
from server.models import OperationResult, TokenType


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/token", tags=["Token"])


@router.get("/generate", response_model=OperationResult)
async def generate_temporary_token() -> OperationResult:
    data = {"type": TokenType.read}
    token = create_token(data)
    logger.info("New token generated.")
    return OperationResult(success=True, data=token)


@router.get("/verify", response_model=OperationResult)
async def verify_token(token: str) -> OperationResult:
    if _verify_token(token):
        return OperationResult(success=True, data=True, message="Valid token.")
    return OperationResult(success=True, data=False, message="Invalid or expired token.")
