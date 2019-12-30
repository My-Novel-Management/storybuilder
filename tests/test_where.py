# -*- coding: utf-8 -*-
"""Test: where.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle
## local files
from builder.where import Where


_FILENAME = "where.py"


class WhereTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Where class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = Where()
        self.assertIsInstance(tmp, Where)

