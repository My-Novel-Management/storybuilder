# -*- coding: utf-8 -*-
"""Test: basecontainer.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import __PRIORITY_NORMAL__
from builder.basecontainer import BaseContainer
from tests import __BASE_ID__


_FILENAME = "basecontainer.py"


class BaseContainerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "BaseContainer class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("title", "data", "dataId", "priority")
        data = [
                (False, ("test",("a",)),
                    ("test", ("a",), __BASE_ID__ + 9, __PRIORITY_NORMAL__)),
                ]
        def _checkcode(vals, expects):
            tmp = BaseContainer(*vals)
            self.assertIsInstance(tmp, BaseContainer)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_inherited(self):
        data = [
                (False, "test", ("apple", "orange")),
                ]
        def _checkcode(title, data):
            tmp = BaseContainer(title, data)
            self.assertIsInstance(tmp, BaseContainer)
            tmp1 = tmp.inherited()
            self.assertIsInstance(tmp1, BaseContainer)
            self.assertEqual(tmp1.title, title)
            self.assertEqual(tmp1.data, data)
        validatedTestingWithFail(self, "inherited", _checkcode, data)
