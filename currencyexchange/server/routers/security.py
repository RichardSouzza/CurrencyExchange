import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from server.exceptions import InvalidTokenException
from server.infrastructure.logger import setup_logging
from server.infrastructure.security import create_token, get_playload, header_scheme
from server.models import OperationResult
from server.models import TokenData


setup_logging()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/token", tags=["Token"])


@router.get("/generate", response_model=OperationResult)
async def generate_temporary_token() -> OperationResult:
    data = {"type": "read"}
    token = await create_token(data)
    logger.info(f"New token generated: {token}")
    return OperationResult(success=True, data=token)


@router.get("/verify", response_model=OperationResult)
async def verify_token(token: str) -> OperationResult:
    payload = get_playload(token)
    if payload:
        return OperationResult(success=True, data=True, message="Valid token.")
    return OperationResult(success=True, data=False, message="Invalid token.")


async def get_active_token(token: Annotated[str, Depends(header_scheme)]) -> TokenData:
    payload = await get_playload(token)
    if payload:
        token_type = payload.get("type")
        if token_type:
            return TokenData(type=token_type)
    raise InvalidTokenException()
