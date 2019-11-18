# -*- coding: utf-8 -*-
"""Test: story.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import story as st
from builder.chapter import Chapter


_FILENAME = "story.py"


class StoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Story class")

    def test_attributes(self):
        data = [
                (False, "test", (Chapter("apple"),),),
                (False, "test", (),),
                (True, 1, (Chapter("apple"),),),
                (True, "test", [1,2,3],),
                ]
        def _checkcode(title, chaps):
            tmp = st.Story(title, *chaps)
            self.assertIsInstance(tmp, st.Story)
            self.assertEqual(tmp.title, title)
            self.assertEqual(tmp.chapters, chaps)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        data = [
                (False, (Chapter("apple"),),),
                (True, [1,2,3],),
                ]
        def _checkcode(chaps):
            tmp = st.Story("test")
            tmp1 = tmp.inherited(*chaps)
            self.assertIsInstance(tmp1, st.Story)
            self.assertEqual(tmp1.chapters, chaps)
        validated_testing_withfail(self, "inherited", _checkcode, data)
