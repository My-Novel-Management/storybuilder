# -*- coding: utf-8 -*-
"""Test: word.py
"""
import unittest
from testutils import print_test_title
from builder.word import Word


_FILENAME = "word.py"


class WordTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Word class")

    def test_attributes(self):
        data = [
                ("test", "a test", "a test", False),
                ("test", None, Word.__NOTE__, False),
                (1, 1, 1, True),
                ]
        def _checkcode(name, note, expect):
            tmp = Word(name, note) if note else Word(name)
            self.assertIsInstance(tmp, Word)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.note, expect)
        for name, note, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(name, note, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(name, note, expect)
