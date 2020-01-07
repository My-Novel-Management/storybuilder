# -*- coding: utf-8 -*-
"""Test: util_math.py
"""
import unittest
from testutils import printTestTitle, validatedTestingWithFail
from utils.util_math import intCeiled


_FILENAME = "util_math.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "math utility")

    def test_intCeiled(self):
        data = [
                (False, 1, 2, 1),
                ]
        validatedTestingWithFail(self, "intCeiled", lambda a, b, expect: self.assertEqual(
            intCeiled(a, b), expect), data)
