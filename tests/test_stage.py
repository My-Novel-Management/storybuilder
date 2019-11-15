# -*- coding: utf-8 -*-
"""Test: stage.py
"""
import unittest
from testutils import print_test_title
from builder import stage as st
from builder.item import Item


_FILENAME = "stage.py"


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Stage class")

    def test_attributes(self):
        data = [
                ("test", "a test", "a test", False),
                ("test", None, st.Stage.__NOTE__, False),
                (1, "a test", "a test", True),
                ]
        def _check_create(name, note, expect):
            tmp = st.Stage(name, note) if note else st.Stage(name)
            self.assertIsInstance(tmp, st.Stage)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.note, expect)
            self.assertEqual(tmp.items, ())
        for name, note, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _check_create(name, note, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _check_create(name, note, expect)

    def test_add(self):
        data = [
                ((Item("apple"),), False),
                ([1,2,3], True),
                ]
        def _checkcode(items):
            tmp = st.Stage("test", "a test")
            self.assertEqual(tmp.items, ())
            tmp.add(*items)
            self.assertEqual(tmp.items, items)
            tmp.add(*items)
            self.assertEqual(tmp.items, items + items)
        for items, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(items)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(items)

    def test_inherited(self):
        base_name, base_note = "test", "a test"
        data = [
                ("apple", "an apple", "apple", "an apple", False),
                ("apple", None, "apple", base_note, False),
                (1, "an apple", 1, "an apple", True),
                ]
        def _checkcode(name1, note1, name2, note2):
            tmp = st.Stage(base_name, base_note)
            tmp1 = tmp.inherited(name1, note1) if note1 else tmp.inherited(name1)
            self.assertIsInstance(tmp1, st.Stage)
            self.assertEqual(tmp1.name, name2)
            self.assertEqual(tmp1.note, note2)
        for name, note, exp_name, exp_note, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(name, note, exp_name, exp_note)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(name, note, exp_name, exp_note)
