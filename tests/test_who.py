# -*- coding: utf-8 -*-
"""Test: who.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle
## local files
from builder.who import Who


_FILENAME = "who.py"


class WhoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Who class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = Who()
        self.assertIsInstance(tmp, Who)

