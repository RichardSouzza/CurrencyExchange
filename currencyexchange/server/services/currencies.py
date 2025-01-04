from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.results import InsertOneResult, UpdateResult

from models.currency import Currency
from models.operation_result import OperationResult


class CurrenciesService:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database.get_collection("currencies")

    async def get_all_currencies(self) -> list[Currency]:
        return await self.collection.find().to_list()

    async def get_currency(self, code: str) -> Currency | None:
        return await self.collection.find_one({"code": code})

    async def set_currency(self, currency: Currency) -> InsertOneResult:
        return await self.collection.insert_one(currency.model_dump())

    async def update_currency(self, currency: Currency) -> UpdateResult:
        return await self.collection.update_one({"code": currency.code}, currency.model_dump())
