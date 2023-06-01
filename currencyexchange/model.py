import datetime
import os
from json import load
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from requests import get


path = os.path.dirname(__file__)
username = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_ACCESS_KEY")
uri = f"mongodb+srv://{username}:{password}@cluster.tendgdt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))
database = client["cluster"]
collection = database["currencies"]


class CEModel:
    def __init__(self, base_currency="USD"):
        self.base_currency = base_currency
        self.documents = list(self.get_documents())
        self.currencies = list(self.get_currencies_codes())
        self.colors = self.get_colors()
    
    def get_chart_data(self, currency) -> list:
        history = self.get_currency_data(self.base_currency)["history"]
        dates = list(history)
        quotes = [value[currency] for value in history.values()]
        chart_color = self.colors[currency]
        return [dates, quotes, chart_color]

    @staticmethod
    def get_colors() -> list:
        with open(os.path.join(path, "static/assets/data/colors.json")) as colors:
            return load(colors)
    
    def get_currencies_data(self):
        for currency in self.currencies:
            yield (
                currency, self.get_currency_rate(currency), self.get_currency_status(currency)
            )
    
    def get_currencies_codes(self):
        for document in self.documents:
            yield document.get("code", "ERROR")
    
    def get_currency_data(self, currency) -> dict:
        data = [document for document in self.documents if document["code"] == currency][0]
        return data

    def get_currency_history(self, base_currency, apikey) -> dict:
        url = "https://api.freecurrencyapi.com/v1/historical"
        today = datetime.date.today()
        date_from = today - datetime.timedelta(days=7)
        date_to = today - datetime.timedelta(days=1)
        params = {
            "apikey": apikey,
            "date_from": date_from,
            "date_to": date_to,
            "base_currency": base_currency
        }
        resp = get(url, params=params)
        data = resp.json()["data"]
        
        for date, history in data.items():
            difference = list(set(self.currencies) - set(history.keys()))
            if any(difference):
                data[date][difference[0]] = 0
                data[date] = dict(sorted(data[date].items()))
            for currency, rate in history.items():
                data[date][currency] = round(rate, 4)
        
        return data
    
    def get_currency_info(self, currency) -> dict:
        document = self.get_currency_data(currency)
        info = {
          "Name": document["name"],
          "Symbol": document["symbol_native"]
        }
        return info
    
    def get_currency_rate(self, currency, date=-1) -> list:
        history = self.get_currency_data(self.base_currency)["history"]
        last_date = list(history)[date]
        rate = history[last_date][currency]
        return rate
    
    def get_currency_status(self, currency) -> str:
        before = float(self.get_currency_rate(currency, -2))
        after = float(self.get_currency_rate(currency))
        if before < after:
            return "increase"
        elif before == after:
            return "stability"
        else:
            return "decrease"
    
    @staticmethod
    def get_documents(filter={}, projection={}) -> object:
        return collection.find(filter, projection)
    
    def set_data(self, apikey) -> None:
        url = "https://api.freecurrencyapi.com/v1/currencies"
        params = {"apikey": apikey}
        resp = get(url, params=params)
        if resp.status_code != 200:
            raise Exception(resp.json().get("message", f"Error {resp.status_code}"))
        data = resp.json()["data"]
        data = dict(sorted(data.items()))
        
        print("Writing documents...")
        
        for count, currency in enumerate(data.keys()):
            loading = f"Loading {data[currency]['name']} data..."
            print(f"{loading} {'[':>{40-len(loading)}}{count+1}/{len(self.currencies)}]")
            data[currency]["history"] = self.get_currency_history(currency, apikey)
        
        documents = list(data.values())
        collection.delete_many({})
        collection.insert_many(documents)

        print("Finished process.")
