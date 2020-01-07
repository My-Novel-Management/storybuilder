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
        data = [
                (False, "test", "a test",
                    "a test",),
                ]
        def _checkcode(name, info, expect):
            tmp = Word(name, info) if info else Word(name)
            self.assertIsInstance(tmp, Word)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.data, expect)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

