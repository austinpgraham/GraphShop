#!/usr/bin/env python3
import os

from sqlalchmey import create_engine

class ModelDB():
    """
    Implementation of the database connection service
    to the relational DB
    """

    _CONFIG_PATH = "cfg/db.cfg"

    def __init__(self, **kwargs):
        conn_str = self._read_cfg()
        self._engine = create_engine(conn_str, connect_args=kwargs)
        self.session = sessionmaker(bind=self._engine, expire_on_commit=False)()
    
    def _read_cfg(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, self._CONFIG_PATH)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()
        self.close()
