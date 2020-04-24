from functools import reduce
import subprocess
import json
import requests
from errors import *


API_URL = "http://localhost:6000"


def start():
    subprocess.run("clear")
    while True:
        print("I - Iniciar carrinho")
        print("S - Sair")
        key = input("> ")
        if key == "I":
            start_cart()

        if key == "S":
            break


def start_cart():
    products = []
    while True:
        subprocess.run("clear")
        show_products(products)

        print("Pressione F para finalizar o carrinho.")
        key = input("Código do produto: ")
        if key == "F":
            break

        try:
            product = get_product(key)
            products.append(product)
        except ProductNotFoundError:
            print("Produto não encontrado")    

    total = reduce(lambda a, b: a + b, [p["price"] for p in products])
    print("Total: {0:.2f}".format(total))
    print()

    while True:
        while True:
            pay_method = input("Forma de pagamento: (D/C)")
            if pay_method in ["D", "C"]:
                break

        try:
            next_step = pay(pay_method, total)
            if next_step == "cash":
                exchange = pay_cash(total)
                print("Troco: {0:.2f}".format(exchange))
            elif next_step == "card":
                pay_card(total)
                print("Pagamento aprovado")

            break
        except PaymentNotApprovedError as e:
            print("Pagamento não aprovado: {}".format(str(e)))

    register_sale(products)
    print("Finalizado")
    print()


def show_products(products):
    if len(products) > 0:
        print("Carrinho:")
        for p in products:
            print("{0:20s} {1}".format(p["name"], p["price"]))
        print()
        print("Subtotal: {0:.2f}".format(reduce(lambda a, b: a + b, [p["price"] for p in products])))
        print()


def get_product(barcode):
    r = requests.get("{}/product/{}".format(API_URL, barcode))
    if r.status_code != 200:
        raise ProductNotFoundError(r.json())

    return r.json()


def register_sale(products):
    r = requests.post("{}/registersale".format(API_URL), json=products)
    if r.status_code != 200:
        print("Erro {}: {}".format(r.status_code, r.json()))


def pay_cash(total):
    while True:
        try:
            value = float(input("Valor em dinheiro: "))
            break
        except ValueError:
            pass

    r = requests.post(
        "{}/paycash".format(API_URL), json={"value": value, "total": total}
    )
    if r.status_code == 400:
        raise PaymentNotApprovedError(r.json()["error"])
    elif r.status_code != 200:
        print("Erro {}: {}".format(r.status_code, r.json()))
    else:
        return r.json()["exchange"]


def pay_card(total):
    number = input("Número do cartão: ")

    r = requests.post(
        "{}/paycard".format(API_URL), json={"card_number": number, "total": total}
    )
    if r.status_code == 400:
        pass
    elif r.status_code != 200:
        print("Erro {}: {}".format(r.status_code, r.json()))

    ret = r.json()
    if not ret["approved"]:
        raise PaymentNotApprovedError(ret["reason"])


def pay(method, value):
    r = requests.post(
        "{}/payment".format(API_URL), json={"method": method, "value": value}
    )
    if r.status_code != 200:
        print("Erro {}: {}".format(r.status_code, r.json()))

    return r.json()["next_step"]


if __name__ == "__main__":
    start()
