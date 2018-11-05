#!/usr/bin/env python3
import os
import json
import unittest

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import add_products

from gs.dataserver.model.review import Review
from gs.dataserver.model.review import add_reviews

from gs.dataserver.model.user import ReviewUser
from gs.dataserver.model.user import add_reviewusers

from gs.views import *


class WebTest(unittest.TestCase):

    TEST_DB = "test.db"
    CONFIG_PATH = "../../dataserver/model/cfg/db.cfg"

    def _add_products(self):
        prod1 = Product(asin='0123456748',
                        title='testbleh',
                        price=56.7,
                        imURL='testurl',
                        brand='testbrand',
                        related='["testrelated"]',
                        salesrank='["testsalesrank"]',
                        categories='["testcat"]')
        prod2 = Product(asin='0123456788',
                        title='testprod',
                        price=56.7,
                        imURL='testurl',
                        brand='testbrand',
                        related='["testrelated"]',
                        salesrank='["testsalesrank"]',
                        categories='["testcat"]')
        add_products([prod1, prod2])
    
    def _add_reviews(self):
        ru = ReviewUser(id='1235',
                        name='TestName')
        r = Review(reviewerID=ru.id,
                   asin='0123456788')
        add_reviewusers([ru])
        add_reviews([r])

    def _write_cfg(self):
        path = os.path.join(os.path.dirname(__file__), self.CONFIG_PATH)
        args = {
            "conn_str": "sqlite:///{}".format(self.TEST_DB)
        }
        json.dump(args, open(path, 'w'))

    def setUp(self):
        open(self.TEST_DB, 'w').close()
        self._write_cfg()
        self._add_products()
        self._add_reviews()
        self.app = application.test_client()

    def tearDown(self):
        os.remove(self.TEST_DB)
        path = os.path.join(os.path.dirname(__file__), self.CONFIG_PATH)
        os.remove(path)
