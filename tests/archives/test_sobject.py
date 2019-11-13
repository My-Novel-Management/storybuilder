# -*- coding: utf-8 -*-
"""Test: sobject.py
"""
import unittest
from builder.testutils import print_test_title
from builder import sobject as so


_FILENAME = "sobject.py"


class SObjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "SObject class")

    def test_attributes(self):
        self.assertIsInstance(so.SObject(), so.SObject)

    def test_eq(self):
        base = so.SObject()
        typeA = so.SObject()
        typeA.added = "test"
        typeB = so.SObject()
        typeB.added = "test"
        data = [
                (base, base, True),
                (base, typeA, False),
                (base, typeB, False),
                (typeA, typeB, True),
                ]

        for v, other, expected in data:
            with self.subTest(v=v, other=other, expected=expected):
                self.assertEqual(v == other, expected)

