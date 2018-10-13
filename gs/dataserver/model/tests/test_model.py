#!/usr/bin/env python3
from hamcrest import raises
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

from gs.dataserver.model.tests import DatabaseTest

from gs.dataserver.model import ModelDB

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import add_products
from gs.dataserver.model.product import get_products


class TestModel(DatabaseTest):

    def test_database(self):
        assert_that(ModelDB(), is_not(raises(Exception)))
        with ModelDB() as _:
            pass

    def test_product(self):
        prod1 = Product(asin='0123456789',
                        title='testprod',
                        price=56.7,
                        imURL='testurl',
                        brand='tesrbrand',
                        related='testrelated',
                        salesrank='testsalesrank',
                        categories='testcat')
        prod2 = Product(asin='0123456788',
                        title='testprod',
                        price=56.7,
                        imURL='testurl',
                        brand='tesrbrand',
                        related='testrelated',
                        salesrank='testsalesrank',
                        categories='testcat')
        add_products([prod1, prod2])
        prods = get_products([prod1.asin, prod2.asin])
        assert_that(prods, has_length(2))
