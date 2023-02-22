import datetime
from json import dumps, load
from requests import get


class CEModel:
    def __init__(self, base_currency="USD"):
        self.base_currency = base_currency
        self.data = self.get_data()
        self.currencies = list(self.data.keys())
        self.colors = self.get_colors()
    
    @staticmethod
    def format_value(value):
        return f"{value:,.2f}".replace(",", " ")
    
    def get_chart_data(self, currency):
        data = self.data[self.base_currency]["history"]
        dates = list(data)
        quotes = [value[currency] for value in data.values()]
        chart_color = self.colors[currency]
        return [dates, quotes, chart_color]
    
    @staticmethod
    def get_colors():
        with open("currencyexchange/static/assets/data/colors.json") as colors:
            return load(colors)
    
    def get_currencies(self):
        for currency, data in self.data.items():
            rate = self.get_rate(currency)
            status = self.get_status(currency)
            yield currency, rate, status
    
    @staticmethod
    def get_data():
        with open("currencyexchange/data.json", "r") as data:
            return load(data)
    
    def get_history(self, base_currency, apikey):
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
    
    def get_info(self, currency):
        data = self.data[currency]
        info = {
          "Name": data["name"],
          "Symbol": data["symbol_native"]
        }
        return info
    
    def get_rate(self, currency, date=-1):
        data = self.data[self.base_currency]
        last = list(data["history"])[date]
        rate = data["history"][last][currency]
        return rate
    
    def get_status(self, currency):
        before = float(self.get_rate(currency, -2))
        after = float(self.get_rate(currency))
        if before < after:
            return "increase"
        elif before == after:
            return "stability"
        else:
            return "decrease"
    
    def set_data(self, apikey):
        url = "https://api.freecurrencyapi.com/v1/currencies"
        params = {"apikey": apikey}
        resp = get(url, params=params)
        data = resp.json()["data"]
        data = dict(sorted(data.items()))
        
        print("Writing data.json...")
        
        for count, currency in enumerate(data.keys()):
            loading = f"Loading {data[currency]['name']} data..."
            print(f"{loading} {'[':>{40-len(loading)}}{count+1}/{len(self.currencies)}]")
            data[currency]["history"] = self.get_history(currency, apikey)
        
        json_object = dumps(data, ensure_ascii=False, indent=4)
        with open("currencyexchange/data.json", "w") as data:
            data.write(json_object)
        
        print("Finished process.")
