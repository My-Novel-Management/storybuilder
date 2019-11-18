# -*- coding: utf-8 -*-
"""Test: item.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import item as it


_FILENAME = "item.py"


class ItemTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Item class")

    def test_attributes(self):
        data = [
                (False, "test", "a note", "a note",),
                (False, "test", None, it.Item.__NOTE__,),
                (True, 1, "a note", "a note",),
                (True, "test", 1, 1,),
                ]
        def _checkcode(name, note, expect):
            tmp = it.Item(name, note) if note else it.Item(name)
            self.assertIsInstance(tmp, it.Item)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.note, expect)
        validated_testing_withfail(self, "attributes", _checkcode, data)

