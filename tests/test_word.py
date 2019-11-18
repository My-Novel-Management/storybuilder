# -*- coding: utf-8 -*-
"""Test: word.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.word import Word


_FILENAME = "word.py"


class WordTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Word class")

    def test_attributes(self):
        data = [
                (False, "test", "a test", "a test",),
                (False, "test", None, Word.__NOTE__,),
                (True, 1, 1, 1,),
                ]
        def _checkcode(name, note, expect):
            tmp = Word(name, note) if note else Word(name)
            self.assertIsInstance(tmp, Word)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.note, expect)
        validated_testing_withfail(self, "attributes", _checkcode, data)
