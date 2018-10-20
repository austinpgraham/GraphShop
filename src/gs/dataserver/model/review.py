#!/usr/bin/env python3
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from gs.dataserver.model import Base
from gs.dataserver.model import _batch
from gs.dataserver.model import ModelDB

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import PRODUCT_ID_LENGTH

from gs.dataserver.model.user import ReviewUser
from gs.dataserver.model.user import USER_ID_LENGTH


class Review(Base):

    __tablename__ = 'review'

    reviewerID = Column(String(USER_ID_LENGTH), ForeignKey("user.id"), primary_key=True)
    asin = Column(String(PRODUCT_ID_LENGTH), ForeignKey("product.asin"), primary_key=True)
    helpful = Column(String)
    text = Column(String)
    overall = Column(Float)
    summary = Column(String)
    time = Column(Integer)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def reviewfunc(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "review" not in db.inspector.get_table_names():
                Base.metadata.create_all(db._engine)
        return func(*args, **kwargs)
    return wrapper


@reviewfunc
def add_reviews(objs, batch_size=50):
    with ModelDB() as db:
        for b in _batch(objs, batch_size):
            db.session.bulk_save_objects(b)


@reviewfunc
def get_reviews(rids=None, pids=None):
    with ModelDB() as db:
        query = db.session.query(Review)
        if rids is not None:
            query = query.filter(Review.reviewerID.in_(rids))
        if pids is not None:
            query = query.filter(Review.asin.in_(pids))
    return query.all()


@reviewfunc
def review_exists(rid, pid):
    with ModelDB() as db:
        query = db.session.query(Review).filter(Review.reviewerID == rid).filter(Review.asin == pid)
    return db.session.query(query.exists()).all().pop()[0]
