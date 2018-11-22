#!/usr/bin/env python3
from flask import Flask

from flask_cors import CORS

from gs.views.product import register_products

application = Flask(__name__)
CORS(application)
register_products(application)
