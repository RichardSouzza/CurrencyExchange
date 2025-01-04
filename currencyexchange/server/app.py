from contextlib import asynccontextmanager

from dotenv import dotenv_values
from fastapi import FastAPI

from core.database import Database
from routers.currencies import router
from services.currencies import CurrenciesService


settings = dotenv_values()


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(
        uri=settings.get("URI") or "",
        db_name=settings.get("DB_NAME") or ""
    )
    await database.connect()
    app.state.currencies_service = CurrenciesService(database.database)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
