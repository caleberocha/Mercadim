
from errors import *


PRODUCTS = [
    {
        'name': 'Arroz', 
        'price': 4.0
    },
    {
        'name': 'Ovo', 
        'price': 10.6
    },
    {
        'name': 'Álcool em gel', 
        'price': 40.0
    },
    {
        'name': 'Sabão', 
        'price': 10.0
    },
    {
        'name': 'Corona', 
        'price': 5.99
    },
]


def get_product(barcode):
    try:
        return PRODUCTS[barcode]
    except (IndexError, ValueError):
        raise ProductNotFoundError(f"Produto {barcode} nao encontrado")