#!/usr/bin/env python3
import json

from flask import Response
from flask import Blueprint

from gs.dataserver.model.product import get_products

PRODUCTS_ROUTE = Blueprint("products", __name__)


@PRODUCTS_ROUTE.route('/<pid>', methods=['GET'])
def get_product(pid):
    pids = set(pid.split('&')) if '&' in pid else [pid]
    products = [p.__dict__ for p in get_products(pids)]
    for p in products:
        p.pop('_sa_instance_state')
    return Response(json.dumps(products, skipkeys=True), mimetype="application/json")


def register_products(app):
    app.register_blueprint(PRODUCTS_ROUTE, url_prefix="/products")
