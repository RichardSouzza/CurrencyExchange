import os
from json import load
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from requests import get


path = os.path.dirname(__file__)
username = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_ACCESS_KEY")
uri = f"mongodb+srv://{username}:{password}@cluster.tendgdt.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))
database = client["cluster"]
collection = database["currencies"]


class CEModel:
    def __init__(self, base_currency="USD"):
        self.base_currency = base_currency
        self.documents = self.get_documents()
        self.currencies = list(self.get_currencies_codes())
        self.colors = self.get_colors()
    
    @staticmethod
    def close_database_connection():
        client.close()
    
    def get_chart_data(self, currency) -> list:
        history = self.get_currency_history(currency)
        dates = list(history)
        quotes = [value[currency] for value in history.values()]
        chart_color = self.colors[currency]
        return dates, quotes, chart_color

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
    
    def get_currency_document(self, currency) -> dict:
        for document in self.documents:
            if document["code"] == currency:
                return document

    def get_currency_history(self, currency) -> dict:
        document = self.get_currency_document(currency)
        history = document["history"]
        return history
    
    def get_new_currency_history(self, base_currency) -> dict:
        lowercase_base_currency = base_currency.lower()
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{lowercase_base_currency}.json"
        resp = get(url)
        data = resp.json()
        rates = self.filter_data(data, lowercase_base_currency)
        history = self.get_currency_history(base_currency)
        new_history = {**history, **{data["date"]: rates}}
        return new_history
    
    def get_currency_info(self, currency) -> dict:
        document = self.get_currency_document(currency)
        info = {
          "Name": document["name"],
          "Symbol": document["symbol_native"]
        }
        return info
    
    def get_currency_name(self, currency) -> str:
        document = self.get_currency_document(currency)
        return document["name"]

    def get_currency_rate(self, currency, date=-1) -> list:
        history = self.get_currency_history(currency)
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
        cursor = collection.find(filter, projection).sort("code", 1)
        documents = list(cursor)
        cursor.close()
        return documents

    def filter_data(self, data, base_currency):
        filtered_data = {}
        for key, value in data[base_currency].items():
            if key.upper() in self.currencies:
                filtered_data[key.upper()] = value
        return filtered_data

    def update_data(self) -> None:
        print("Updating documents...")
        
        for count, currency in enumerate(self.currencies):
            currency_name = self.get_currency_name(currency)
            loading = f"Loading {currency_name} data..."
            print(f"{loading} {'[':>{40-len(loading)}}{count+1}/{len(self.currencies)}]")
            history = self.get_new_currency_history(currency)
            collection.update_one({"code": currency}, {"$set": {"history": history}})
        
        print("Finished process.")
