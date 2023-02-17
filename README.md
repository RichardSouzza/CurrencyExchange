# CurrencyExchange
A Flask-based website that shows data for the world's major currencies.

Link: [CurrencyExchange](https://currencyexchange.onrender.com/)

## Features
- Built with [Flask](https://flask.palletsprojects.com/) framework
- Hosted on the [Render](https://render.com/) platform
- Powered by data from [FreeCurrencyAPI](https://freecurrencyapi.com/)

## Installation
1. Clone the repository:
```yaml
git clone https://github.com/RichardSouzza/CurrencyExchange
```
2. Access the project folder:
```yaml
cd CurrencyExchange
```
3. Install the dependencies:
```yaml
pip install -r requirements.txt
```
4. Start the app:
```yaml
python run.py
```

## API
The Currency Exchange makes currency data available through its API.

### Endpoints
#### Currencies Endpoint
Returns the data of all 33 available currencies.

**Request Method:** GET

**Request URL:** `https://currency-exchange-rxpg.onrender.com/currencies`

**Request Parameters**

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Mandatory</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>currencies</code></td>
    <td>string</td>
    <td></td>
    <td>
      A list of comma seperated currency
      codes which you want to get (EUR,USD,CAD)
      By default all available currencies will be shown
    </td>
  </tr>
</table>

**Sample Request**
```python
from requests import get
from json import dumps

url = "https://currencyexchange.onrender.com/currencies"

params = {
    "currencies": "EUR, GBP, USD"
}

resp = get(url, params=params)

data = resp.json()

print(dumps(data, indent=4))
```

**Sample Response**

```json
{
    "USD": {
        "symbol": "$",
        "name": "US Dollar",
        "symbol_native": "$",
        "decimal_digits": 2,
        "rounding": 0,
        "code": "USD",
        "name_plural": "US dollars",
        "history": {
            "2023-01-29": {
                "AUD": 1.4069,
                "BGN": 1.7978,
                "BRL": 5.1092,
                "..."
                "TRY": 18.8126,
                "USD": 1,
                "ZAR": 17.2094
            },
            "2023-01-30": {
                "AUD": 1.4171,
                "BGN": 1.7997,
                "BRL": 5.1163,
                "..."
                "TRY": 18.813,
                "USD": 1,
                "ZAR": 17.3935
            },
            "..."
            "2023-02-03": {
                "AUD": 1.4443,
                "BGN": 1.8121,
                "BRL": 5.1525,
                "..."
                "TRY": 18.8199,
                "USD": 1,
                "ZAR": 17.4675
            },
            "2023-02-04": {
                "AUD": 1.4447,
                "BGN": 1.8093,
                "BRL": 5.1518,
                "..."
                "TRY": 18.8236,
                "USD": 1,
                "ZAR": 17.4678
            }
        }
    }
}
```
