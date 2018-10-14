#!/usr/bin/env python3
import os
import json
import unittest


class DatabaseTest(unittest.TestCase):

    TEST_DB = "test.db"
    CONFIG_PATH = "../cfg/db.cfg"

    def _write_cfg(self):
        path = os.path.join(os.path.dirname(__file__), self.CONFIG_PATH)
        args = {
            "conn_str": "sqlite:///{}".format(self.TEST_DB)
        }
        json.dump(args, open(path, 'w'))

    def setUp(self):
        open(self.TEST_DB, 'w').close()
        self._write_cfg()

    def tearDown(self):
        os.remove(self.TEST_DB)
        path = os.path.join(os.path.dirname(__file__), self.CONFIG_PATH)
        os.remove(path)
