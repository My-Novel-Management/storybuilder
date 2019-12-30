# -*- coding: utf-8 -*-
"""Test: extractor.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
from utils.util_compare import equalsContainers
## local file_
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.extractor import Extractor
from builder.scene import Scene
from builder.story import Story
from builder.shot import Shot


_FILENAME = "extractor.py"


class ExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Extractor class")

    def setUp(self):
        pass

    def test_attributes(self):
        data = [
                (False, Story("test"),),
                ]
        def _checkcode(v):
            tmp = Extractor(v)
            self.assertIsInstance(tmp, Extractor)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_story(self):
        s1 = Story("test")
        data = [
                (False, s1, s1),
                (False, Chapter("1"), Story(Extractor.__NO_DATA__)),
                ]
        def _checkcode(v, expect):
            self.assertTrue(equalsContainers(Extractor(v).story, expect))
        validatedTestingWithFail(self, "story", _checkcode, data)

    def test_chapters(self):
        ch1, ch2 = Chapter("1"), Chapter("2")
        data = [
                (False, Story("test", ch1, ch2), (ch1, ch2)),
                (False, Story("test"), ()),
                (False, ch1, (ch1,)),
                (False, Episode("e1"), ()),
                (False, Scene("s1"), ()),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).chapters, expect)
        validatedTestingWithFail(self, "chapters", _checkcode, data)

    def test_episodes(self):
        ep1, ep2 = Episode("1"), Episode("2")
        data = [
                (False, Story("test", Chapter("c1", ep1, ep2)),
                    (ep1, ep2)),
                (False, Story("test", Chapter("c1", ep1), Chapter("c2", ep2)),
                    (ep1, ep2)),
                (False, Chapter("c1", ep1), (ep1,)),
                (False, ep1, (ep1,)),
                (False, Scene("s1"), ()),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).episodes, expect)
        validatedTestingWithFail(self, "episodes", _checkcode, data)

    def test_scenes(self):
        sc1, sc2 = Scene("s1"), Scene("s2")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", sc1, sc2))),
                    (sc1, sc2)),
                (False, Chapter("c1", Episode("e1", sc1), Episode("e2", sc2)),
                    (sc1, sc2)),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).scenes, expect)
        validatedTestingWithFail(self, "scenes", _checkcode, data)

    def test_actions(self):
        ac1, ac2 = Action("a"), Action("b")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", ac1, ac2)))),
                    (ac1, ac2)),
                (False, Episode("e1", Scene("s1", ac1), Scene("s2", ac2)),
                    (ac1, ac2)),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).actions, expect)
        validatedTestingWithFail(self, "actions", _checkcode, data)

    def test_alldirections(self):
        sh1 = Shot("orange")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a","apple", "orange"))))),
                    ("apple", "orange")),
                (False, Scene("test", Action("a","apple"), Action("a",sh1)),
                    ("apple", sh1)),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).alldirections, expect)
        validatedTestingWithFail(self, "alldirections", _checkcode, data)

    def test_directions(self):
        sh1 = Shot("orange")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a","apple", "orange"))))),
                    ("apple", "orange")),
                (False, Scene("test", Action("a","apple"), Action("a",sh1)),
                    ("apple",)),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).directions, expect)
        validatedTestingWithFail(self, "directions", _checkcode, data)

    def test_shots(self):
        sh1, sh2 = Shot("orange"), Shot("melon")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a","apple", "orange"))))),
                    ()),
                (False, Scene("test", Action("a","apple"), Action("a",sh1, sh2)),
                    (sh1, sh2)),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Extractor(v).shots, expect)
        validatedTestingWithFail(self, "shots", _checkcode, data)
