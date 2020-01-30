# -*- coding: utf-8 -*-
"""Test: area.py
"""
## public libs
import math
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.area import Area


_FILENAME = "area.py"


class AreaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Area class")

    def setUp(self):
        pass

    def test_attributes(self):
        data = [
                (False, ("test", "T", 1, 1, "a place"), ("test", "T", (1,1), "a place")),
                ]
        def _checkcode(vals, expect):
            tmp = Area(*vals)
            self.assertIsInstance(tmp, Area)
            self.assertEqual(tmp.tag, expect[0])
            self.assertEqual(tmp.name, expect[1])
            self.assertEqual(tmp.data, expect[2])
            self.assertEqual(tmp.note, expect[3])
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_distance(self):
        data = [
                (False, ("A", "a", 1,1), ("B", "b", 2,2), math.sqrt(2)),
                ]
        def _checkcode(val1, val2, expect):
            tmp1, tmp2 = Area(*val1), Area(*val2)
            self.assertEqual(tmp1.distance(tmp2), expect)
        validatedTestingWithFail(self, "distance", _checkcode, data)
