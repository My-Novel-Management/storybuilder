# -*- coding: utf-8 -*-
"""Test: story.py
"""
import unittest
from testutils import print_test_title
from builder import story as st
from builder.chapter import Chapter


_FILENAME = "story.py"


class StoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Story class")

    def test_attributes(self):
        data = [
                ("test", (Chapter("apple"),), False),
                ("test", (), False),
                (1, (Chapter("apple"),), True),
                ("test", [1,2,3], True),
                ]
        for title, chaps, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = st.Story(title, *chaps)
                    self.assertIsInstance(tmp, st.Story)
                    self.assertEqual(tmp.title, title)
                    self.assertEqual(tmp.chapters, chaps)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = st.Story(title, *chaps)
                        self.assertIsInstance(tmp, st.Story)
                        self.assertEqual(tmp.title, title)
                        self.assertEqual(tmp.chapters, chaps)

    def test_inherited(self):
        data = [
                ((Chapter("apple"),), False),
                ([1,2,3], True),
                ]
        for chaps, isfail in data:
            with self.subTest():
                tmp = st.Story("test")
                if not isfail:
                    tmp1 = tmp.inherited(*chaps)
                    self.assertIsInstance(tmp1, st.Story)
                    self.assertEqual(tmp1.chapters, chaps)
                else:
                    with self.assertRaises(AssertionError):
                        tmp1 = tmp.inherited(*chaps)
                        self.assertIsInstance(tmp1, st.Story)
                        self.assertEqual(tmp1.chapters, chaps)
