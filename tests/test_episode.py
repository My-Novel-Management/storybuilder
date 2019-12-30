# -*- coding: utf-8 -*-
"""Test: episode.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.episode import Episode
from builder.scene import Scene


_FILENAME = "episode.py"


class EpisodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Episode class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("scenes", "note")
        sc1 = Scene("apple")
        sc2 = Scene("orange")
        data = [
                (False, "test", (sc1, sc2), "a test",
                    ((sc1, sc2), "a test")),
                ]
        def _checkcode(title, vals, note, expects):
            tmp = Episode(title, *vals, note=note)
            self.assertIsInstance(tmp, Episode)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

