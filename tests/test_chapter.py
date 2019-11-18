# -*- coding: utf-8 -*-
"""Test: chapter.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import chapter as ch

_FILENAME = "chapter.py"


class ChapterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Chapter class")

    def test_attributes(self):
        from builder.episode import Episode
        data = [
                (False, "test", (Episode("test", "a test"),),),
                (False, "test", (),),
                (True, 1, (Episode("test", "a test"),),),
                (True, "test", ("test", "a test"),),
                ]
        def _checkcode(title, eps):
            tmp = ch.Chapter(title, *eps)
            self.assertIsInstance(tmp, ch.Chapter)
            self.assertEqual(tmp.episodes, eps)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        from builder.episode import Episode
        data = [
                (False, (Episode("1", "a test"), Episode("2", "an apple")),),
                (False, (),),
                (True, [1,2,3],),
                ]
        def _checkcode(eps):
            tmp = ch.Chapter("test", Episode("test", "a test"))
            tmp1 = tmp.inherited(*eps)
            self.assertIsInstance(tmp1, ch.Chapter)
            self.assertEqual(tmp1.episodes, eps)
        validated_testing_withfail(self, "inherited", _checkcode, data)
