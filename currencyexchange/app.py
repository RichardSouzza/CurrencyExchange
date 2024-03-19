from flask import Flask, abort, jsonify, render_template, request
from currencyexchange.model import CEModel


app = Flask(__name__)
model = CEModel()


@app.route("/")
@app.route("/<base_currency>")
def home(base_currency="USD"):
    base_currency = base_currency.upper()
    if base_currency not in model.currencies:
        abort(404)
    else:
        model.base_currency = base_currency
    
    return render_template(
        "home.html",
        title="CurrencyExchange",
        base_currency=base_currency,
        model=model
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        title="About – CurrencyExchange"
    )


@app.route("/api")
def api():
    return render_template(
        "api.html",
        title="API – CurrencyExchange"
    )


@app.route("/currencies", methods=["GET"])
def get_currencies():
    currencies = request.args.get(
        "currencies", default=",".join(model.currencies), type=str
    ).replace(" ", "").split(",")
    
    filter_query = {"code": {"$in": currencies}}
    projection_query = {"_id": 0}
    documents = model.get_documents(filter_query, projection_query)
    documents = {document["code"]: document for document in documents}
    return jsonify(documents)


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        title="404 – CurrencyExchange"
    ), 404


@app.teardown_request
def close_database_connection(error):
    if not request.path.startswith("/static/"):
        model.close_database_connection()
