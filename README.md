# CurrencyExchange
A Flask-based website that shows data for the world's major currencies.

Link: [CurrencyExchange](https://currencyexchange.onrender.com/)

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FRichardSouzza%2FCurrencyExchange&countColor=%23263759)

## Features
- Built with [Flask](https://flask.palletsprojects.com/) framework
- Hosted on the [Render](https://render.com/) platform
- Powered by data from [FreeCurrencyAPI](https://freecurrencyapi.com/)
- Store API data on [MongoDB Atlas](https://www.mongodb.com/atlas/database)

## API
The CurrencyExchange makes currency data available through its API.

### Endpoints
#### Currencies Endpoint
Returns data for selected currencies.

**Request Method:** GET

**Request URL:** `https://currencyexchange.onrender.com/currencies`

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
      A list of comma separated currency
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
    "currencies": "EUR, USD, CAD"
}

resp = get(url, params=params)

data = resp.json()

print(dumps(data, indent=4))
```

**Sample Response**

```json
{
    "EUR": {
        "code": "EUR",
        "decimal_digits": 2,
        "history": {
            "2023-05-24": {
                "AUD": 1.6434,
                "BGN": 1.9536,
                "BRL": 5.3349,
                "..."
                "TRY": 21.4166,
                "USD": 1.0756,
                "ZAR": 20.696
            },
            "2023-05-25": {
                "AUD": 1.6503,
                "BGN": 1.9556,
                "BRL": 5.4014,
                "..."
                "TRY": 21.4261,
                "USD": 1.0724,
                "ZAR": 21.2226
            },
            "..."
            "2023-05-29": {
                "AUD": 1.6402,
                "BGN": 1.9557,
                "BRL": 5.3746,
                "..."
                "TRY": 21.5727,
                "USD": 1.0707,
                "ZAR": 21.0558
            },
            "2023-05-30": {
                "AUD": 1.6465,
                "BGN": 1.9556,
                "BRL": 5.4046,
                "..."
                "TRY": 22.1244,
                "USD": 1.0731,
                "ZAR": 21.1276
            }
        },
        "name": "Euro",
        "name_plural": "Euros",
        "rounding": 0,
        "symbol": "€",
        "symbol_native": "€"
    }
}
```
