from flask import Flask, request


CARDS = ["000000", "111111", "222222"]

app = Flask(__name__)


@app.route("/paycash", methods=["POST"])
def pay_cash():
    data = request.json
    print(data)

    if data["value"] < data["total"]:
        return {"error": "Valor insuficiente"}, 400

    return {"exchange": data["value"] - data["total"]}


@app.route("/paycard", methods=["POST"])
def pay_card():
    data = request.json
    print(data)

    if not data["card_number"] in CARDS:
        return {"approved": False, "reason": "Cartao nao encontrado"}, 400

    return {"approved": True, "reason": ""}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6100)
