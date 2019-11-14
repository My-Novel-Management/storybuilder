# -*- coding: utf-8 -*-
"""Test: episode.py
"""
import unittest
from testutils import print_test_title
from builder import episode as ep

_FILENAME = "episode.py"


class EpisodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Episode class")

    def test_attributes(self):
        from builder.scene import Scene
        sc1 = Scene("test", "a test")
        data = [
                ("test", "a test", (sc1,), False),
                (1, "a test", (sc1,), True),
                ("test", 1, (sc1,), True),
                ("test", "a test", [1,], True),
                ]
        for title, outline, scs, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = ep.Episode(title, outline, *scs)
                    self.assertIsInstance(tmp, ep.Episode)
                    self.assertEqual(tmp.title, title)
                    self.assertEqual(tmp.outline, outline)
                    self.assertEqual(tmp.scenes, scs)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = ep.Episode(title, outline, *scs)
                        self.assertIsInstance(tmp, ep.Episode)
                        self.assertEqual(tmp.title, title)
                        self.assertEqual(tmp.outline, outline)
                        self.assertEqual(tmp.scenes, scs)

    def test_inherited(self):
        from builder.scene import Scene
        sc1 = Scene("test1", "an apple")
        sc2 = Scene("test2", "a orange")
        data = [
                ((sc1, sc2), False),
                ([1,2], True),
                ]
        for scenes, isfail in data:
            with self.subTest():
                tmp = ep.Episode("test", "a test")
                if not isfail:
                    tmp1 = tmp.inherited(*scenes)
                    self.assertIsInstance(tmp1, ep.Episode)
                    self.assertEqual(tmp1.scenes, scenes)
                else:
                    with self.assertRaises(AssertionError):
                        tmp1 = tmp.inherited(*scenes)
                        self.assertIsInstance(tmp1, ep.Episode)
                        self.assertEqual(tmp1.scenes, scenes)
