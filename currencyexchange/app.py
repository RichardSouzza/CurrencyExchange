from flask import Flask, abort, jsonify, render_template, request
from currencyexchange.model import CEModel


app = Flask(__name__)


@app.route("/")
@app.route("/<base_currency>")
def home(base_currency="USD"):
    base_currency = base_currency.upper()
    model = CEModel(base_currency)
    
    if base_currency not in model.currencies:
      abort(404)
    
    return render_template(
        "home.html",
        title="Currency Exchange",
        base_currency=base_currency,
        model=model
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        title="About – Currency Exchange"
    )


@app.route("/api")
def api():
    return render_template(
        "api.html",
        title="API – Currency Exchange"
    )


@app.route("/currencies", methods=["GET"])
def get_currencies():
    model = CEModel()
    currencies = request.args.get(
        "currencies", default=",".join(model.currencies), type=str
    ).replace(" ", "").split(",")
    
    data = {}
    for currency in currencies:
        if currency in model.currencies:
            data[currency] = model.data[currency]
    
    return jsonify(data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        title="404 – Currency Exchange"
    ), 404
