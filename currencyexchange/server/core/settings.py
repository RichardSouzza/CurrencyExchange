from os import getenv

from dotenv import load_dotenv


load_dotenv()

ATLAS_USER     = getenv("ATLAS_USER")     or ""
ATLAS_PASSWORD = getenv("ATLAS_PASSWORD") or ""
ATLAS_CLUSTER  = getenv("ATLAS_CLUSTER")  or ""
ATLAS_DATABASE = getenv("ATLAS_DATABASE") or ""

ATLAS_URI      = f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASSWORD}@{ATLAS_CLUSTER}.mongodb.net/?retryWrites=true&w=majority"

available_currencies = [
    "aud", "bgn", "brl", "cad", "chf", "cny", "czk", "dkk", "eur", "gbp", "hkd",
    "hrk", "huf", "idr", "ils", "inr", "isk", "jpy", "krw", "mxn", "myr", "nok",
    "nzd", "php", "pln", "ron", "rub", "sek", "sgd", "thb", "try", "usd", "zar",
]
