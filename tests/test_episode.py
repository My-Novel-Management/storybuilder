# -*- coding: utf-8 -*-
"""Test: episode.py
"""
import unittest
from testutils import print_test_title ,validated_testing_withfail
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
                (False, "test", "a test", (sc1,),),
                (True, 1, "a test", (sc1,),),
                (True, "test", 1, (sc1,),),
                (True, "test", "a test", [1,],),
                ]
        def _checkcode(title, outline, scs):
            tmp = ep.Episode(title, outline, *scs)
            self.assertIsInstance(tmp, ep.Episode)
            self.assertEqual(tmp.title, title)
            self.assertEqual(tmp.outline, outline)
            self.assertEqual(tmp.scenes, scs)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        from builder.scene import Scene
        sc1 = Scene("test1", "an apple")
        sc2 = Scene("test2", "a orange")
        data = [
                (False, (sc1, sc2),),
                (True, [1,2],),
                ]
        def _checkcode(scenes):
            tmp = ep.Episode("test", "a test")
            tmp1 = tmp.inherited(*scenes)
            self.assertIsInstance(tmp1, ep.Episode)
            self.assertEqual(tmp1.scenes, scenes)
        validated_testing_withfail(self, "inherited", _checkcode, data)
