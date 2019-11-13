# -*- coding: utf-8 -*-
"""Test: stage.py
"""
import unittest
from testutils import print_test_title
from builder import stage as st


_FILENAME = "stage.py"


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Stage class")

    def test_attributes(self):
        s = st.Stage("test stage")
        self.assertIsInstance(s, st.Stage)
        self.assertEqual(s.name, "test stage")

    def test_method_add(self):
        data = [
                ((st.Item("t1"),), 1),
                ((st.Item("t1"), st.Item("t2")), 2),
                ]
        for items, num in data:
            with self.subTest(items=items, num=num):
                s = st.Stage("test stage")
                res = s.add(*items)
                self.assertEqual(len(res.items), num)
