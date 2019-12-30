# -*- coding: utf-8 -*-
"""Test: basedata.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from tests import __BASE_ID__
from builder.basedata import BaseData


_FILENAME = "basedata.py"


class BaseDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "BaseData class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("name", "data", "dataId")
        data = [
                (False, ("test",("a",)),
                    ("test", ("a",), __BASE_ID__ - 12)),
                ]
        def _checkcode(vals, expects):
            tmp = BaseData(*vals)
            self.assertIsInstance(tmp, BaseData)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

