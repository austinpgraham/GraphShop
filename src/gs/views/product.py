#!/usr/bin/env python3
from flask import Blueprint


PRODUCTS_ROUTE = Blueprint("products", __name__)


@PRODUCTS_ROUTE.route('/<pid>', methods=['GET'])
def get_product(pid):
    return ""


def register_products(app):
    app.register_blueprint(PRODUCTS_ROUTE, url_prefix="/products")
