from contextlib import asynccontextmanager
from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI

from server.infrastructure.database import Database
from server.routers.currencies import router as currencies_router
from server.routers.security import router as security_router
from server.services.currencies import CurrenciesService


load_dotenv()

ATLAS_USER     = getenv("ATLAS_USER")     or ""
ATLAS_PASSWORD = getenv("ATLAS_PASSWORD") or ""
ATLAS_CLUSTER  = getenv("ATLAS_CLUSTER")  or ""
ATLAS_DATABASE = getenv("ATLAS_DATABASE") or ""

ATLAS_URI      = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASSWORD}@{ATLAS_CLUSTER}.mongodb.net/?retryWrites=true&w=majority"

@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(
        uri=ATLAS_URI,
        db_name=ATLAS_DATABASE
    )
    await database.connect()
    app.state.currencies_service = CurrenciesService(database.database)
    yield
    await database.disconnect()


app = FastAPI(title="CurrencyExchange", lifespan=lifespan)
app.include_router(currencies_router)
app.include_router(security_router)
