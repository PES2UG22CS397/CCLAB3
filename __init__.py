from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> "Product":
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


def list_products() -> list[Product]:
    return [Product.load(product) for product in dao.list_products()]


def get_product(product_id: int) -> Product:
    return Product.load(dao.get_product(product_id))


def add_product(product: dict):
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)


import cart
import products
from cart import get_cart
import os

def checkout(username):
    cart = get_cart(username)
    total = 0
    for item in cart:
        total += item.cost

    #Here the exit can happen when a illegal memory is accessed 
    # or when a error is not handled properly
    #os._exit(1)
    return total


def complete_checkout(username):
    cartv = cart.get_cart(username)
    items = cartv
    for item in items:
        assert item.qty >= 1
    for item in items:
        cart.delete_cart(username)
        products.update_qty(item.id, item.qty-1)

import json
from typing import List
import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(
            id=data["id"],
            username=data["username"],
            contents=[Product(**item) for item in json.loads(data["contents"])],
            cost=data["cost"],
        )


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    all_products = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail["contents"])
        except json.JSONDecodeError:
            continue  # Skip invalid JSON contents
        all_products.extend(products.get_product(item) for item in contents)
    
    return all_products


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)

