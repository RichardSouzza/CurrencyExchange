import logging
from datetime import date, datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorDatabase

from server.core.settings import available_currencies as desired_currencies
from server.exceptions import *
from server.models import CurrencyDocument, CurrencyRequest, OperationResult, SetCurrencyDocument
from server.services.external import ExternalService
from server.utils.parsers import parse_date_to_datetime


logger = logging.getLogger(__name__)


class CurrenciesService:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database.get_collection("currencies")
        self.external_service = ExternalService()

    async def get_currencies_in_range(self, request: CurrencyRequest) -> list[CurrencyDocument]:
        start_date = datetime.now() - timedelta(days=request.range)
        end_date = datetime.now()
        result = await self.collection.find({"date": {"$gte": start_date, "$lte": end_date}}).to_list()
        return [CurrencyDocument(**currency) for currency in result]

    async def get_currencies_in_range_by_code(self, request: CurrencyRequest) -> list[CurrencyDocument]:
        start_date = datetime.now() - timedelta(days=request.range)
        end_date = datetime.now()
        result = await self.collection.find({"code": request.code, "date": {"$gte": start_date, "$lte": end_date}}).to_list()
        return [CurrencyDocument(**currency) for currency in result]

    async def get_currency(self, request: CurrencyRequest) -> CurrencyDocument | None:
        return await self.collection.find_one({"code": request.code, "date": parse_date_to_datetime(request.date)})

    async def register_currency(self, currency: CurrencyDocument | SetCurrencyDocument) -> OperationResult:
        logger.info(f"Setting {currency.code.upper()} data...")

        existing_currency = await self.get_currency(CurrencyRequest(code=currency.code, date=currency.date))
        if existing_currency:
            logger.info(f"Currency {currency.code.upper()} already exists for date {currency.date}.")
            raise CurrencyAlreadyExistsException()

        result = await self.collection.insert_one(currency.model_dump())

        logger.info(f"Currency {currency.code.upper()} registered successfully!")
        return OperationResult(success=True, message=f"Currency {currency.code.upper()} registered successfully!")

    async def update_currency(self, currency: CurrencyDocument) -> OperationResult:
        logger.info(f"Updating {currency.code.upper()} data...")

        result = await self.collection.update_one({"code": currency.code, "date": currency.date}, currency.model_dump())

        if result.matched_count == 0:
            logger.info(f"Currency {currency.code.upper()} not found for update.")
            raise CurrencyNotFoundException()
        if result.modified_count > 0:
            logger.info(f"Currency {currency.code.upper()} updated successfully!")
        
        return OperationResult(success=True, message=f"Currency {currency.code.upper()} updated successfully!")

    async def daily_currencies_update(self, request: CurrencyRequest) -> OperationResult:
        logger.info("Updating currencies...")

        for base in desired_currencies:
            existing_currency = await self.get_currency(CurrencyRequest(code=base, date=request.date))
            if existing_currency:
                logger.info(f"Currency {base.upper()} already exists for date {request.date}. Skipping update.")
            else:
                response = await self.external_service.get_currencies_with_base_by_date(base, request.date)
                currencies = response.model_dump()
                filtered_currencies = {}

                for currency, value in currencies[base].items():
                    if currency in desired_currencies:
                        filtered_currencies[currency] = value

                currencies[base] = filtered_currencies
                currencyDocument = SetCurrencyDocument(code=base, **currencies)
                await self.register_currency(currencyDocument)

        logger.info("Daily currencies updated successfully!")
        return OperationResult(success=True, message=f"Daily currencies updated successfully for date {date.strftime(request.date, '%Y-%m-%d')}!")
