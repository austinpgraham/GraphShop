#!/usr/bin/env python3
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Column

from gs.dataserver.model import Base
from gs.dataserver.model import ModelDB


PRODUCT_ID_LENGTH = 10


class Product(Base):

    __tablename__ = "product"

    asin = Column(String(PRODUCT_ID_LENGTH), primary_index=True)
    title = Column(String)
    price = Column(Float)
    imURL = Column(String)
    brand = Column(String)
    related = Column(String)
    salesRank = Column(String)
    categories = Column(String)


def productfunc(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "product" not in db.inspector.get_table_names():
                Base.metadata.create_all()
        return func(*args, **kwargs)
    return wrapper


@productfunc
def add_product(obj):
    pass
