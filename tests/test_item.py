# -*- coding: utf-8 -*-
"""Test: item.py
"""
import unittest
from testutils import print_test_title
from builder import item as it


_FILENAME = "item.py"


class ItemTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Item class")

    def test_attributes(self):
        data = [
                ("test", "a note", "a note", False),
                ("test", None, it.Item.__NOTE__, False),
                (1, "a note", "a note", True),
                ("test", 1, 1, True),
                ]
        for name, note, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = it.Item(name, note) if note else it.Item(name)
                    self.assertIsInstance(tmp, it.Item)
                    self.assertEqual(tmp.name, name)
                    self.assertEqual(tmp.note, expect)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = it.Item(name, note) if note else it.Item(name)
                        self.assertIsInstance(tmp, it.Item)
                        self.assertEqual(tmp.name, name)
                        self.assertEqual(tmp.note, expect)

