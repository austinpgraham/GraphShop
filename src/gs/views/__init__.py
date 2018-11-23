#!/usr/bin/env python3
from flask import Flask

from flask_cors import CORS

from gs.views.product import register_products

from gs.views.reviews import register_reviews

application = Flask(__name__)
CORS(application)
register_products(application)
register_reviews(application)
