#!/usr/bin/env python3
from hamcrest import raises
from hamcrest import is_not
from hamcrest import assert_that

from gs.dataserver.model.tests import DatabaseTest

from gs.dataserver.model import ModelDB


class TestModel(DatabaseTest):

    def test_database(self):
        try:
            assert_that(ModelDB(), is_not(raises(Exception)))
        finally:
            self.tearDown()

