from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class Database:
    def __init__(self, uri: str, db_name: str) -> None:
        self.uri = uri
        self.db_name = db_name

    async def connect(self) -> None:
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.database = self.client.get_database(self.db_name)
            await self.client.admin.command("ping")
            print("SUCCESS: Conectado ao MongoDB com sucesso!")
        except Exception as error:
            print(f"ERROR: Falha ao conectar ao MongoDB: {error}")
            raise error

    async def disconnect(self) -> None:
        if self.client:
            self.client.close()
            print("INFO: Database connection closed!")

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection[Any]:
        return self.database.get_collection(collection_name)
