# -*- coding: utf-8 -*-
"""Test: basecontainer.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import __PRIORITY_NORMAL__, __PRIORITY_MIN__
from builder.basecontainer import BaseContainer


_FILENAME = "basecontainer.py"


class BaseContainerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "BaseContainer class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("title", "data", "note", "priority")
        data = [
                (False, "test", ("a",), "apple",
                    ("test", ("a",), "apple", __PRIORITY_NORMAL__)),
                ]
        def _checkcode(title, data, note, expects):
            tmp = BaseContainer(title, *data, note=note)
            self.assertIsInstance(tmp, BaseContainer)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_dataId(self):
        tmp = BaseContainer("test", ("a",))
        self.assertIsInstance(tmp.dataId, int)

    def test_inherted(self):
        tmp = BaseContainer("test", ("apple", "orange"), note="a note", priority=1)
        self.assertEqual(tmp.title, "test")
        self.assertEqual(tmp.data, ("apple","orange"))
        self.assertEqual(tmp.note, "a note")
        self.assertEqual(tmp.priority, 1)
        tmp1 = tmp.inherited("orange")
        self.assertEqual(tmp1.title, "test")
        self.assertEqual(tmp1.data, ("orange",))
        self.assertEqual(tmp1.note, "a note")
        self.assertEqual(tmp1.priority, 1)

    def test_omit(self):
        tmp = BaseContainer("test")
        self.assertEqual(tmp.priority, __PRIORITY_NORMAL__)
        tmp.omit()
        self.assertEqual(tmp.priority, __PRIORITY_MIN__)
