import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pymongo.results import InsertOneResult

from models.currency import Currency
from services.currencies import CurrenciesService
from server.core.logger import setup_logging


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
    
    response = await currencies_service.set_currency(currency)
    logger.info("Data set successfully!")
    return response
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
