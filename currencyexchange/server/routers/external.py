from datetime import date, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from server.exceptions import OnlyAdminException
from server.infrastructure.security import get_active_token
from server.models import Currency, ExternalCurrency, TokenData, TokenType
from server.services import ExternalService


router = APIRouter(prefix="/api/external", tags=["External"])


@router.get("/currencies", response_model=list[Currency])
async def get_all_available_currencies(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
) -> list[Currency]:
    """
    Lists all the available currencies in prettified json format.
    """
    if token.type != TokenType.write:
            raise OnlyAdminException("access external services")

    external_service: ExternalService = request.app.state.external_service
    return await external_service.get_all_available_currencies()


@router.get("/currenciesWith/{base_currency}", response_model=ExternalCurrency)
async def get_currencies_with_base(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        base_currency: str,
) -> ExternalCurrency:
    """
    Get the currency list with `base_currency` as base on the current date.
    """
    if token.type != TokenType.write:
            raise OnlyAdminException("access external services")

    external_service: ExternalService = request.app.state.external_service
    return await external_service.get_currencies_with_base(base_currency.lower())

@router.get("/currenciesByDateWith/{base_currency}", response_model=ExternalCurrency)
async def get_currencies_with_base_by_date(
        token: Annotated[TokenData, Depends(get_active_token)],
        request: Request,
        base_currency: str,
        date: date = datetime.now().date(),
) -> ExternalCurrency:
    """
    Get the currency list with `base_currency` as base on date `date`.
    """
    if token.type != TokenType.write:
            raise OnlyAdminException("access external services")

    external_service: ExternalService = request.app.state.external_service
    return await external_service.get_currencies_with_base_by_date(base_currency.lower(), date)
