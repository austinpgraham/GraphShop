#!/usr/bin/env python3
import json

from sqlalchemy import or_
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Column

from gs.dataserver.model import Base
from gs.dataserver.model import _batch
from gs.dataserver.model import ModelDB


PRODUCT_ID_LENGTH = 10


class Product(Base):
    """
    ORM object for the Product entity.
    """

    __tablename__ = "product"

    asin = Column(String(PRODUCT_ID_LENGTH), primary_key=True, unique=True)
    title = Column(String)
    price = Column(Float)
    imURL = Column(String)
    brand = Column(String)
    related = Column(String)
    salesRank = Column(String)
    categories = Column(String)

    _JSON_ATTS = [
        "related",
        "salesRank",
        "categories"
    ]

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def convert_json(self):
        """
        Convert the object to JSON
        """
        for att in self._JSON_ATTS:
            val = getattr(self, att, "[]") or "[]"
            val = val.replace("'", '"')
            try:
                setattr(self, att, json.loads(val))
            except: # pragma: no cover
                self.att = []


def productfunc(func, *args, **kwargs):
    """
    Check for the existence of the table,
    create if it does not exist.
    """
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "product" not in db.inspector.get_table_names():
                Base.metadata.create_all(db._engine)
        return func(*args, **kwargs)
    return wrapper


@productfunc
def add_products(objs, batch_size=50):
    """
    Add a set of products
    """
    with ModelDB() as db:
        for b in _batch(objs, batch_size):
            db.session.bulk_save_objects(b)


@productfunc
def get_products(ids):
    """
    Get a set of products
    """
    with ModelDB() as db:
        result = db.session.query(Product).filter(Product.asin.in_(ids)).all()
    for r in result:
        r.convert_json()
    return result


@productfunc
def product_exists(asin):
    """
    Return if a product is present in the database.
    """
    with ModelDB() as db:
        query = db.session.query(Product).filter(Product.asin == asin)
        ans = db.session.query(query.exists()).all().pop()[0]
    return ans


@productfunc
def search_products(query_str):
    """
    Return all products that match the
    given query string.
    """
    with ModelDB() as db:
        query = db.session.query(Product).filter(or_(Product.title.like(query_str), Product.brand.like(query_str)))
        result = query.all()
    for _, val in enumerate(result):
        val.convert_json()
    return result


@productfunc
def get_all_ids():
    """
    Get all product IDs in the database.
    """
    with ModelDB() as db:
        query = db.session.query(Product.asin)
        result = query.all()
    return [r[0] for r in result]


@productfunc
def update_product(asin, key, value):
    """
    Update a given product.
    """
    with ModelDB() as db:
        db.session.query(Product).filter(Product.asin == asin).\
            update({key: json.dumps(value)})
