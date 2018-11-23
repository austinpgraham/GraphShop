#!/usr/bin/env python3
from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

from gs.views.tests import WebTest


class TestReviews(WebTest):

    def test_get(self):
        result = self.app.get('/reviews/0123456788')
        assert_that(result.json, has_length(1))
        assert_that(result.json[0]['asin'], is_('0123456788'))

        result = self.app.get('/reviews/recommendations/1235')
        assert_that(result.json, has_length(1))
        assert_that(result.json[0]['userID'], is_('1235'))
