# -*- coding: utf-8 -*-
"""Test: when.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle
## local files
from builder.when import When


_FILENAME = "when.py"


class WhenTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "When class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = When()
        self.assertIsInstance(tmp, When)

