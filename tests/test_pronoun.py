# -*- coding: utf-8 -*-
"""Test: pronoun.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle
## local files
from builder.pronoun import Who, When, Where, That


_FILENAME = "pronoun.py"


class PronounClassesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "pronoun classes")

    def setUp(self):
        pass

    def test_Who(self):
        tmp = Who()
        self.assertIsInstance(tmp, Who)

    def test_Where(self):
        tmp = Where()
        self.assertIsInstance(tmp, Where)

    def test_When(self):
        tmp = When()
        self.assertIsInstance(tmp, When)

    def test_That(self):
        tmp = That()
        self.assertIsInstance(tmp, That)
