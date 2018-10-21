#!/usr/bin/env python3
from flask import Flask

from gs.views.product import register_products

base_app = Flask(__name__)
register_products(base_app)
