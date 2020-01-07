# -*- coding: utf-8 -*-
"""Test: story.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.chapter import Chapter
from builder.story import Story


_FILENAME = "story.py"


class StoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Story class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("data", "note")
        ch1 = Chapter("melon")
        ch2 = Chapter("lemon")
        data = [
                (False, "test", (ch1, ch2), "a test",
                    ((ch1, ch2), "a test")),
                ]
        def _checkcode(title, vals, note, expects):
            tmp = Story(title, *vals, note=note)
            self.assertIsInstance(tmp, Story)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_inherited(self):
        ch1, ch2 = Chapter("apple"), Chapter("orange")
        tmp = Story("test", ch1)
        self.assertEqual(tmp.data, (ch1,))
        tmp1 = tmp.inherited(ch2)
        self.assertEqual(tmp1.data, (ch2,))
