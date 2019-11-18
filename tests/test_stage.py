# -*- coding: utf-8 -*-
"""Test: stage.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import stage as st
from builder.item import Item


_FILENAME = "stage.py"


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Stage class")

    def test_attributes(self):
        data = [
                (False, "test", "a test", "a test",),
                (False, "test", None, st.Stage.__NOTE__,),
                (True, 1, "a test", "a test",),
                ]
        def _checkcode(name, note, expect):
            tmp = st.Stage(name, note) if note else st.Stage(name)
            self.assertIsInstance(tmp, st.Stage)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.note, expect)
            self.assertEqual(tmp.items, ())
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_add(self):
        data = [
                (False, (Item("apple"),),),
                (True, [1,2,3],),
                ]
        def _checkcode(items):
            tmp = st.Stage("test", "a test")
            self.assertEqual(tmp.items, ())
            tmp.add(*items)
            self.assertEqual(tmp.items, items)
            tmp.add(*items)
            self.assertEqual(tmp.items, items + items)
        validated_testing_withfail(self, "add", _checkcode, data)

    def test_inherited(self):
        base_name, base_note = "test", "a test"
        data = [
                (False, "apple", "an apple", "apple", "an apple",),
                (False, "apple", None, "apple", base_note,),
                (True, 1, "an apple", 1, "an apple",),
                ]
        def _checkcode(name1, note1, name2, note2):
            tmp = st.Stage(base_name, base_note)
            tmp1 = tmp.inherited(name1, note1) if note1 else tmp.inherited(name1)
            self.assertIsInstance(tmp1, st.Stage)
            self.assertEqual(tmp1.name, name2)
            self.assertEqual(tmp1.note, note2)
        validated_testing_withfail(self, "inherited", _checkcode, data)
