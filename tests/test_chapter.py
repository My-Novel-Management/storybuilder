# -*- coding: utf-8 -*-
"""Test: chapter.py
"""
import unittest
from testutils import print_test_title
from builder import chapter as ch

_FILENAME = "chapter.py"


class ChapterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Chapter class")

    def test_attributes(self):
        from builder.episode import Episode
        data = [
                ("test", (Episode("test", "a test"),), False),
                ("test", (), False),
                (1, (Episode("test", "a test"),), True),
                ("test", ("test", "a test"), True),
                ]
        for title, eps, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = ch.Chapter(title, *eps)
                    self.assertIsInstance(tmp, ch.Chapter)
                    self.assertEqual(tmp.episodes, eps)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = ch.Chapter(title, *eps)
                        self.assertIsInstance(tmp, ch.Chapter)
                        self.assertEqual(tmp.episodes, eps)

    def test_inherited(self):
        from builder.episode import Episode
        data = [
                ((Episode("1", "a test"), Episode("2", "an apple")), False),
                ((), False),
                ([1,2,3], True),
                ]
        for eps, isfail in data:
            with self.subTest():
                tmp = ch.Chapter("test", Episode("test", "a test"))
                if not isfail:
                    tmp1 = tmp.inherited(*eps)
                    self.assertIsInstance(tmp1, ch.Chapter)
                    self.assertEqual(tmp1.episodes, eps)
                else:
                    with self.assertRaises(AssertionError):
                        tmp1 = tmp.inherited(*eps)
                        self.assertIsInstance(tmp1, ch.Chapter)
                        self.assertEqual(tmp1.episodes, eps)
