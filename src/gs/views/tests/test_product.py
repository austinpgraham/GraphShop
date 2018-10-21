#!/usr/bin/env python3
from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

from gs.views.tests import WebTest

from gs.views.product import *


class TestProducts(WebTest):

    def test_product_get(self):
        result = self.app.get('/products/123')
        assert_that(result.json, is_([]))

        result = self.app.get('/products/0123456748')
        assert_that(result.json.pop()['asin'], is_('0123456748'))

        result = self.app.get('/products/0123456748&0123456788')
        assert_that(result.json, has_length(2))

    def test_product_search(self):
        result = self.app.get('/products/search/*bleh*')
        assert_that(result.json, has_length(1))

        result = self.app.get('/products/search/*test*')
        assert_that(result.json, has_length(2))

        result = self.app.get('/products/search/testbrand')
        assert_that(result.json, has_length(2))
