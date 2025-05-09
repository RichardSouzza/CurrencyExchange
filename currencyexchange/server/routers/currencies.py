import logging
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from server.exceptions import *
from server.infrastructure.security import get_active_token
from server.models import AvailableCurrencies, CurrencyDocument, CurrencyRequest, OperationResult, TokenData, TokenType
from server.services.currencies import CurrenciesService


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Currencies"])


@router.get("/currencies_by_range", response_model=list[CurrencyDocument])
async def get_currencies_in_range(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        range: int
) -> list[CurrencyDocument]:
    params = CurrencyRequest(range=range)
    currencies_service: CurrenciesService = request.app.state.currencies_service
    currencies = await currencies_service.get_currencies_in_range(params)
    return currencies


@router.get("/currencies_by_range/{code}", response_model=list[CurrencyDocument])
async def get_currencies_in_range_by_code(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        code: AvailableCurrencies, # type: ignore
        range: int
) -> list[CurrencyDocument]:
    params = CurrencyRequest(code=code, range=range)
    currencies_service: CurrenciesService = request.app.state.currencies_service
    currencies = await currencies_service.get_currencies_in_range_by_code(params)
    return currencies


@router.get("/currency/{code}", response_model=CurrencyDocument | None)
async def get_currency(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        code: AvailableCurrencies, # type: ignore
        date: date = datetime.now().date(),
) -> CurrencyDocument | None:
    params = CurrencyRequest(code=code, date=date)
    currencies_service: CurrenciesService = request.app.state.currencies_service
    result = await currencies_service.get_currency(params)
    if result is None:
        raise CurrencyNotFoundException()
    return result


@router.post("/currency/{code}", status_code=status.HTTP_201_CREATED)
async def set_currency(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        currency: CurrencyDocument,
) -> OperationResult:
    if token.type != TokenType.write:
        raise OnlyAdminException("register currencies")

    currencies_service: CurrenciesService = request.app.state.currencies_service
    response = await currencies_service.register_currency(currency)
    return response


@router.patch("/currency/{code}")
async def patch_currency(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        currency: CurrencyDocument,
) -> OperationResult:
    if token.type != TokenType.write:
        raise OnlyAdminException("update currencies")

    currencies_service: CurrenciesService = request.app.state.currencies_service
    response = await currencies_service.update_currency(currency)
    return response


@router.post("/currencies/dailyUpdate", status_code=status.HTTP_201_CREATED, response_model=OperationResult)
async def daily_currencies_update(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        date: date = datetime.now().date(),
) -> OperationResult:
    if token.type != TokenType.write:
        raise OnlyAdminException("update currencies")

    currencies_service: CurrenciesService = request.app.state.currencies_service
    response = await currencies_service.daily_currencies_update(CurrencyRequest(date=date))
    return response
