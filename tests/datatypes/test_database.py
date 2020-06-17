# -*- coding: utf-8 -*-
'''
Database class test
===================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import database as db


class DatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(db.__name__, 'Database class')

    def test_instance(self):
        tmp = db.Database()
        self.assertIsInstance(tmp, db.Database)

