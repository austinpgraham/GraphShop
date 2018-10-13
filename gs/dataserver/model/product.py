#!/usr/bin/env python3
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Column

from gs.dataserver.model import Base
from gs.dataserver.model import _batch
from gs.dataserver.model import ModelDB


PRODUCT_ID_LENGTH = 10


class Product(Base):

    __tablename__ = "product"

    asin = Column(String(PRODUCT_ID_LENGTH), primary_key=True, unique=True)
    title = Column(String)
    price = Column(Float)
    imURL = Column(String)
    brand = Column(String)
    related = Column(String)
    salesRank = Column(String)
    categories = Column(String)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def productfunc(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "product" not in db.inspector.get_table_names():
                Base.metadata.create_all(db._engine)
        return func(*args, **kwargs)
    return wrapper


@productfunc
def add_products(objs, batch_size=50):
    with ModelDB() as db:
        for b in _batch(objs, batch_size):
            db.session.bulk_save_objects(b)


@productfunc
def get_products(ids):
    with ModelDB() as db:
        result = db.session.query(Product).filter(Product.asin.in_(ids)).all()
    return result
