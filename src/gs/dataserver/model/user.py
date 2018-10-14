#!/usr/bin/env python3
from sqlalchemy import Column
from sqlalchemy import String

from gs.dataserver.model import Base
from gs.dataserver.model import _batch
from gs.dataserver.model import ModelDB


USER_ID_LENGTH = 14


class ReviewUser(Base):

    __tablename__ = "user"

    id = Column(String(USER_ID_LENGTH), primary_key=True, unique=True)
    name = Column(String)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def reviewuserfunc(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "user" not in db.inspector.get_table_names():
                Base.metadata.create_all(db._engine)
        return func(*args, **kwargs)
    return wrapper


@reviewuserfunc
def add_reviewusers(objs, batch_size=50):
    with ModelDB() as db:
        for b in _batch(objs, batch_size):
            db.session.bulk_save_objects(b)


@reviewuserfunc
def get_reviewusers(ids):
    with ModelDB() as db:
        result = db.session.query(ReviewUser).filter(ReviewUser.id.in_(ids)).all()
    return result
