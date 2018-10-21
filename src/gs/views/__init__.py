#!/usr/bin/env python3
from flask import Flask

from gs.views.product import register_products

application = Flask(__name__)
register_products(application)
