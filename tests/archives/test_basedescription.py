# -*- coding: utf-8 -*-
"""Test: basedescription.py
"""
import unittest
from builder.testutils import print_test_title
from builder import basedescription as bd
from builder import enums as em


_FILENAME = "basedescription.py"


class BaseDescTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseDescription class")

    def test_attributes(self):
        data = [
                (em.DescType.DESCRIPTION, em.DescType.DESCRIPTION),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertIsInstance(bd.BaseDesc(v), bd.BaseDesc)
                self.assertEqual(bd.BaseDesc(v).desc_type, expected)
