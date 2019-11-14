# -*- coding: utf-8 -*-
"""Test: chara.py
"""
import unittest
from testutils import print_test_title
from builder import chara as ch


_FILENAME = "chara.py"


class CharaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Chara class")

    def test_attributes(self):
        data = [
                ("test", False),
                (1, True),
                ]
        for name, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = ch.Chara(name)
                    self.assertIsInstance(tmp, ch.Chara)
                    self.assertEqual(tmp.name, name)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = ch.Chara(name)
                        self.assertIsInstance(tmp, ch.Chara)
                        self.assertEqual(tmp.name, name)

