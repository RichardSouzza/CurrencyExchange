from datetime import date as dt, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_extra_types.mongo_object_id import MongoObjectId

from server.core.settings import available_currencies
from server.utils.parsers import parse_date_to_datetime


AvailableCurrencies = Enum("AvailableCurrencies", {currency: currency for currency in available_currencies}, type=str)


class Currency(BaseModel):
    code: str = Field(max_length=3)
    name: str

    model_config = ConfigDict(frozen=True)


class CurrencyDocument(BaseModel):
    id: MongoObjectId = Field(alias="_id", default_factory=lambda: MongoObjectId(), exclude=True)
    code: str = Field(max_length=3)
    date: datetime
    rates: dict[str, float] = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @classmethod
    @field_validator("date", mode="before")
    def parse_date(cls, value) -> datetime:
        return parse_date_to_datetime(value)


class CurrencyRequest(BaseModel):
    code: str = Field(default="", max_length=3)
    date: dt | datetime = Field(default_factory=lambda: datetime.now())
    range: int = Field(default=1)
    
    @classmethod
    @field_validator("date", mode="before")
    def parse_date(cls, value) -> datetime:
        return parse_date_to_datetime(value)


class ExternalCurrency(BaseModel):
    date: str

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    def parse_rates(cls, values: dict) -> dict[Any, Any]:
        base_currency = ""
        rates = {}

        for key, value in values.items():
            if key != "date":
                base_currency = key
                rates[key] = value

        values[base_currency] = rates.get(base_currency)
        return values


class SetCurrencyDocument(BaseModel):
    id: MongoObjectId = Field(alias="_id", default_factory=lambda: MongoObjectId(), exclude=True)
    code: str = Field(max_length=3)
    date: datetime
    rates: dict[str, float] = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @classmethod
    @field_validator("date", mode="before")
    def parse_date(cls, value) -> datetime:
        return parse_date_to_datetime(value)
    
    @model_validator(mode="before")
    def parse_rates(cls, values: dict) -> dict[Any, Any]:
        base_currency = ""
        rates = {}

        for key, value in values.items():
            if key not in ["code", "date"]:
                base_currency = key
                rates[key] = value

        values["rates"] = rates.get(base_currency)
        return values
