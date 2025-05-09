import logging
from datetime import date

from server.models import Currency, ExternalCurrency
from server.utils import httpx


logger = logging.getLogger(__name__)


class ExternalService:
    def __init__(self) -> None:
        self.base_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0"

    async def get_all_available_currencies(self) -> list[Currency]:
        """
        Lists all the available currencies in prettified json format.
        """
        logger.info("Fetching all available currencies from external API...")

        url = f"{self.base_url}/currency-api@latest/v1/currencies.min.json"

        response = await httpx.get(url)

        currencies = [
            Currency(**response)]

        return currencies

    async def get_currencies_with_base(self, base_currency: str) -> ExternalCurrency:
        """
        Get the currency list with `base_currency` as base.
        """
        logger.info(f"Fetching currencies with base {base_currency} from external API...")

        url = f"{self.base_url}/currency-api@latest/v1/currencies/{base_currency}.min.json"

        response = await httpx.get(url)

        return ExternalCurrency(**response)

    async def get_currencies_with_base_by_date(self, base_currency: str, date: date) -> ExternalCurrency:
        """
        Get the currency list with `base_currency` as base on date `date`.
        """
        logger.info(f"Fetching currencies with base {base_currency} from external API for date {date}...")

        url = f"{self.base_url}/currency-api@{date}/v1/currencies/{base_currency}.min.json"

        response = await httpx.get(url)

        return ExternalCurrency(**response)
