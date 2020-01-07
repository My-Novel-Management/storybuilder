# -*- coding: utf-8 -*-
"""Test: utility.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.action import Action
from builder.conjuction import Then
from builder.utility import hasThen


_FILENAME = "utility.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "utility methods")

    def setUp(self):
        pass

    def test_hasThen(self):
        data = [
                (False, Action("apple", "orange"), False),
                ]
        validatedTestingWithFail(self, "hasThen", lambda v, expect: self.assertEqual(
            hasThen(v), expect), data)

