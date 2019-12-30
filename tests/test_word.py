# -*- coding: utf-8 -*-
"""Test: word.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.word import Word


_FILENAME = "word.py"


class WordTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Word class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("note",)
        data = [
                (False, "test", "a test",
                    ("a test",)),
                ]
        def _checkcode(name, note, expects):
            tmp = Word(name, note)
            self.assertIsInstance(tmp, Word)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

