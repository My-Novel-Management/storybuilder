# -*- coding: utf-8 -*-
"""Test: item.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.item import Item


_FILENAME = "item.py"


class ItemTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Item class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("note",)
        data = [
                (False, "test", "a test",
                    ("a test",)),
                ]
        def _checkcode(name, note, expects):
            tmp = Item(name, note)
            self.assertIsInstance(tmp, Item)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

