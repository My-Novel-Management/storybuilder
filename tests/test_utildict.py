# -*- coding: utf-8 -*-
"""Test: utildict.py
"""
import unittest
from testutils import printTestTitle, validatedTestingWithFail
from utils.utildict import UtilityDict


_FILENAME = "utildict.py"


class UtilityDictTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "UtilityDict class")

    def test_attributes(self):
        tmp = UtilityDict()
        tmp.__setitem__("a", "apple")
        self.assertTrue(hasattr(tmp, "a"))
        self.assertEqual(tmp.a, "apple")
