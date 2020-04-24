from flask import Flask, request
import requests
from errors import *
import dbo

CARDS_API_URL = "http://localhost:6100"

app = Flask(__name__)


@app.route("/product/<barcode>")
def get_product(barcode):
    try:
        return dbo.get_product(int(barcode))
    except (ProductNotFoundError, ValueError) as e:
        return {"error": str(e)}, 400


@app.route("/registersale", methods=["POST"])
def register_sale():
    data = request.json
    print(data)

    return {"success": True}


@app.route("/payment", methods=["POST"])
def pay():
    data = request.json
    print(data)

    if data["method"] == "D":
        return {"next_step": "cash"}

    if data["method"] == "C":
        return {"next_step": "card"}


@app.route("/paycash", methods=["POST"])
def pay_cash():
    data = request.json
    print(data)

    r = requests.post("{}/paycash".format(CARDS_API_URL), json=data)
    return r.json(), r.status_code


@app.route("/paycard", methods=["POST"])
def pay_card():
    data = request.json
    print(data)

    r = requests.post("{}/paycard".format(CARDS_API_URL), json=data)
    return r.json(), r.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
