# -*- coding: utf-8 -*-
"""Test: basedata.py
"""
import unittest
from testutils import print_test_title
from builder import basedata as bs


_FILENAME = "basedata.py"


class BaseDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseData class")

    def test_attributes(self):
        data = [
                ("test", False),
                (1, True),
                ]
        for name, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = bs.BaseData(name)
                    self.assertIsInstance(tmp, bs.BaseData)
                    self.assertEqual(tmp.name, name)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = bs.BaseData(name)

class NoDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "NoData class")

    def test_attributes(self):
        tmp = bs.NoData()
        self.assertIsInstance(tmp, bs.NoData)
        self.assertEqual(tmp.name, bs.NoData.__NAME__)
