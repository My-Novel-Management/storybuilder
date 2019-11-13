# -*- coding: utf-8 -*-
"""Test: prson.py
"""
import unittest
from testutils import print_test_title
from builder import person as psn


_FILENAME = "person.py"


class PersonTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Person class")

    def test_attributes(self):
        p = psn.Person("Taro", "Yamada, Taro", 17, "male", "student",
                "me:俺", "a man", "hair:黒")
        self.assertIsInstance(p, psn.Person)
        self.assertEqual(p.name, "Taro")
        self.assertEqual(p.age, 17)
        self.assertEqual(p.sex, "male")
        self.assertEqual(p.job, "student")
        self.assertEqual(p.calling, {"me": "俺", "S":"Taro", "M":"俺"})
        self.assertEqual(p.note, "a man")
        self.assertEqual(p.features, {"hair": "黒"})

