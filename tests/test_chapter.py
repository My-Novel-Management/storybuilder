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
        c = ch.Chapter("test title")
        self.assertTrue(isinstance(c, ch.Chapter))
        self.assertEqual(c.title, "test title")

    @unittest.skip("wip")
    def test_method_add(self):
        data = [
                ((ch.Scene("s1"),), 1),
                ((ch.Scene("s1"), ch.Scene("s2")), 2),
                ]

        for scenes, num in data:
            with self.subTest(scenes=scenes, num=num):
                c = ch.Chapter("test chapter")
                res = c.add(*scenes)
                self.assertEqual(len(res.scenes), num)
