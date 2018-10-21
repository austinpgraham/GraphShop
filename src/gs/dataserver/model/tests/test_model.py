#!/usr/bin/env python3
from hamcrest import is_
from hamcrest import raises
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

from gs.dataserver.model.tests import DatabaseTest

from gs.dataserver.model import ModelDB

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import add_products
from gs.dataserver.model.product import get_products
from gs.dataserver.model.product import product_exists
from gs.dataserver.model.product import search_products

from gs.dataserver.model.user import ReviewUser
from gs.dataserver.model.user import user_exists
from gs.dataserver.model.user import get_reviewusers
from gs.dataserver.model.user import add_reviewusers

from gs.dataserver.model.review import Review
from gs.dataserver.model.review import add_reviews
from gs.dataserver.model.review import get_reviews
from gs.dataserver.model.review import review_exists


class TestModel(DatabaseTest):

    def test_database(self):
        assert_that(ModelDB(), is_not(raises(Exception)))
        with ModelDB() as _:
            pass

    def test_product(self):
        exists = product_exists('0123456789')
        assert_that(exists, is_(False))
        prod1 = Product(asin='0123456789',
                        title='testbleh',
                        price=56.7,
                        imURL='testurl',
                        brand='tesrbrand',
                        related='["testrelated"]',
                        salesrank='["testsalesrank"]',
                        categories='["testcat"]')
        prod2 = Product(asin='0123456788',
                        title='testprod',
                        price=56.7,
                        imURL='testurl',
                        brand='tesrbrand',
                        related='["testrelated"]',
                        salesrank='["testsalesrank"]',
                        categories='["testcat"]')
        add_products([prod1, prod2])
        prods = get_products([prod1.asin, prod2.asin])
        assert_that(prods, has_length(2))
        assert_that(product_exists('0123456789'), is_(True))

        # Test search
        result = search_products("%prod%")
        assert_that(result, has_length(1))

        result = search_products("%test%")
        assert_that(result, has_length(2))

    def test_user(self):
        exists = user_exists('1234')
        assert_that(exists, is_(False))
        ru = ReviewUser(id='1234',
                        name='TestName')
        add_reviewusers([ru])
        users = get_reviewusers(['1234'])
        assert_that(users, has_length(1))
        exists = user_exists('1234')
        assert_that(exists, is_(True))

    def test_review(self):
        exists = review_exists('1235', '0123456748')
        assert_that(exists, is_(False))
        prod = Product(asin='0123456748',
                       title='testprod',
                       price=56.7,
                       imURL='testurl',
                       brand='tesrbrand',
                       related='["testrelated"]',
                       salesrank='{testsalesrank: 5}',
                       categories='["testcat"]')
        ru = ReviewUser(id='1235',
                        name='TestName')
        r = Review(reviewerID=ru.id,
                   asin=prod.asin)
        add_reviews([r])
        reviews = get_reviews(rids=[ru.id], pids=[prod.asin])
        assert_that(reviews, has_length(1))
        exists = review_exists('1235', '0123456748')
        assert_that(exists, is_(True))
