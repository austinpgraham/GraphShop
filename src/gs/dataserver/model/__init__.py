#!/usr/bin/env python3
import os
import json

from sqlalchemy import inspect
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ModelDB():
    """
    Implementation of the database connection service
    to the relational DB
    """

    _CONFIG_PATH = os.path.dirname(__file__) + "/cfg/db.cfg"

    def __init__(self, **kwargs):
        cfg = self._read_cfg()
        self._engine = create_engine(cfg['conn_str'], connect_args=kwargs)
        self.session = sessionmaker(bind=self._engine, expire_on_commit=False)()

    def _read_cfg(self):
        return json.load(open(self._CONFIG_PATH, 'r'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()
        self.close()

    def close(self):
        self.session.close()

    @property
    def inspector(self):
        return inspect(self._engine)  # pragma: no cover


def _batch(iterable, size):
    l = len(iterable)
    for i in range(0, l, size):
        yield iterable[i:min(i + size, l)]
