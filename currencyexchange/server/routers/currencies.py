import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pymongo.results import InsertOneResult

from server.exceptions import *
from server.infrastructure.logger import setup_logging
from server.models import Currency
from server.models import TokenData
from server.routers.security import get_active_token
from server.services.currencies import CurrenciesService


setup_logging()

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Currencies"])


@router.get("/api/currencies", response_model=list[Currency])
async def get_all_currencies(
        request: Request,
        token: str = Depends(oauth2_scheme)
) -> list[Currency]:
    currencies_service: CurrenciesService = request.app.state.currencies_service
    return await currencies_service.get_all_currencies()


@router.get("/api/currency/{code}", response_model=Currency)
async def get_currency(
        request: Request,
        code: str,
        token: str = Depends(oauth2_scheme)
) -> Currency | None:
    currencies_service: CurrenciesService = request.app.state.currencies_service
    return await currencies_service.get_currency(code)


@router.post("/api/currency/{code}", status_code=201)
async def set_currency(
        request: Request,
        currency: Currency,
        token: str = Depends(oauth2_scheme)
) -> InsertOneResult:
    currencies_service: CurrenciesService = request.app.state.currencies_service

    logger.info(f"Setting {currency.name} data...")

    # if token_data.get("role") != "admin":
    #         raise HTTPException(403, "Only admin users can create currencies.")
    
    existent_currency = await currencies_service.get_currency(currency.code)
    if existent_currency:
        raise HTTPException(409, "There is already a currency with the same code.")
    
    response = await currencies_service.register_currency(currency)
    logger.info(f"Currency {currency.code} registered successfully!")


@router.patch("/api/currency/{code}")
async def patch_currency(
        request: Request,
        currency: Currency,
        token: str = Depends(oauth2_scheme)
) -> None:
    currencies_service: CurrenciesService = request.app.state.currencies_service

    logger.info(f"Updating {currency.name} data...")
    response = await currencies_service.update_currency(currency)
    logger.info(f"Data updated successfully!")
