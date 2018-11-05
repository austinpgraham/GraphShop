#!/usr/bin/env python3
import os
import json
import unittest


class DatabaseTest(unittest.TestCase):

    TEST_DB = "test.db"
    CONFIG_PATH = os.path.dirname(__file__) + "/../cfg/db.cfg"

    def _write_cfg(self):
        path = self.CONFIG_PATH
        args = {
            "conn_str": "sqlite:///{}".format(self.TEST_DB)
        }
        with open(path, 'w') as _file:
            json.dump(args, _file)

    def setUp(self):
        open(self.TEST_DB, 'w').close()
        self._write_cfg()

    def tearDown(self):
        os.remove(self.TEST_DB)
        path = self.CONFIG_PATH
        os.remove(path)
