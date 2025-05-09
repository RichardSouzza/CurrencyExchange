import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.core.settings import *
from server.infrastructure.database import Database
from server.infrastructure.logger import setup_logging
from server.routers import currencies_router, external_router, security_router
from server.services import CurrenciesService, ExternalService


setup_logging()
logging.getLogger("watchfiles").setLevel(logging.CRITICAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(
        uri=ATLAS_URI,
        db_name=ATLAS_DATABASE
    )
    await database.connect()

    app.state.currencies_service = CurrenciesService(database.database)
    app.state.external_service = ExternalService()
    
    yield
    await database.disconnect()


app = FastAPI(
    title="CurrencyExchange",
    summary="An API that provides data for the world's major currencies.",
    version="2.0.0",
    lifespan=lifespan,
    contact={
        "name": "CurrencyExchange",
        "url": "https://github.com/RichardSouzza/CurrencyExchange",
    },
    license_info={
        "name": "Mozilla Public License 2.0",
        "url": "https://github.com/RichardSouzza/CurrencyExchange/blob/master/LICENSE",
    },
)

app.include_router(currencies_router)
app.include_router(external_router)
app.include_router(security_router)
