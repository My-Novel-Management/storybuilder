# -*- coding: utf-8 -*-
"""Test: basedata.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import basedata as bs


_FILENAME = "basedata.py"


class BaseDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseData class")

    def test_attributes(self):
        data = [
                (False, "test",),
                (True, 1,),
                ]
        def _checkcode(name):
            tmp = bs.BaseData(name)
            self.assertIsInstance(tmp, bs.BaseData)
            self.assertEqual(tmp.name, name)
        validated_testing_withfail(self, "attributes", _checkcode, data)

class NoDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "NoData class")

    def test_attributes(self):
        tmp = bs.NoData()
        self.assertIsInstance(tmp, bs.NoData)
        self.assertEqual(tmp.name, bs.NoData.__NAME__)
