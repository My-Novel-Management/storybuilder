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
        data = [
                (False, "test", "a test",
                    "a test",),
                ]
        def _checkcode(name, info, expect):
            tmp = Item(name, info) if info else Item(name)
            self.assertIsInstance(tmp, Item)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.data, expect)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

