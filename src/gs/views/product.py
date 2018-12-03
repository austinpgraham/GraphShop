#!/usr/bin/env python3
import json

from flask import Response
from flask import Blueprint

from gs.dataserver.model.product import get_products
from gs.dataserver.model.product import search_products as sp

PRODUCTS_ROUTE = Blueprint("products", __name__)


@PRODUCTS_ROUTE.route('/<pid>', methods=['GET'])
def get_product(pid):
    """
    Get a series of products
    """
    pids = set(pid.split('&')) if '&' in pid else [pid]
    products = [p.__dict__ for p in get_products(pids)]
    for p in products:
        p.pop('_sa_instance_state')
    return Response(json.dumps(products, skipkeys=True), mimetype="application/json")


@PRODUCTS_ROUTE.route('/search/<query>', methods=['GET'])
def search_products(query):
    """
    Search the database with the given query
    """
    query = query.replace('*', '%')
    products = [p.__dict__ for p in sp(query)]
    for p in products:
        p.pop('_sa_instance_state')
    return Response(json.dumps(products, skipkeys=True), mimetype="application/json")


def register_products(app):
    app.register_blueprint(PRODUCTS_ROUTE, url_prefix="/products")
