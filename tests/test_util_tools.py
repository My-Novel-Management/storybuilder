# -*- coding: utf-8 -*-
"""Test: util_tools.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
import utils.util_tools as util


_FILENAME = "util_tools.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "util tools methods")

    def setUp(self):
        pass

    def test_tupleFiltered(self):
        data = [
                (False, (1,2, "1"), int,
                    (1,2)),
                ]
        validatedTestingWithFail(self, "tupleFiltered",
                lambda v, t, expect: self.assertEqual(
                    util.tupleFiltered(v, t), expect), data)

    def test_tupleEvenStr(self):
        data = [
                (False, "test",
                    ("test",)),
                ]
        validatedTestingWithFail(self, "tupleEvenStar",
                lambda v, expect: self.assertEqual(
                    util.tupleEvenStr(v), expect), data)
