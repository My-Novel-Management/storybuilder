# -*- coding: utf-8 -*-
"""Test: counter.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType
from builder.action import Action
from builder.chapter import Chapter
from builder.counter import Counter
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


_FILENAME = "counter.py"


class CounterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Counter class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = Counter(Story("test"))
        self.assertIsInstance(tmp, Counter)

    def test_countChapter(self):
        data = [
                (False, Story("test", Chapter("1"), Chapter("2")),
                    2),
                (False, Chapter("test"),
                    1),
                (False, Episode("test"), 0),
                (False, Scene("test"), 0),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Counter(v).countChapter(), expect)
        validatedTestingWithFail(self, "countChapter", _checkcode, data)

    def test_countEpisode(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("1"), Episode("2"))),
                    2),
                (False, Chapter("c1", Episode("1")), 1),
                (False, Episode("1"), 1),
                (False, Scene("1"), 0),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Counter(v).countEpisode(), expect)
        validatedTestingWithFail(self, "countEpisode", _checkcode, data)

    def test_countScene(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", Scene("1"), Scene("2")))),
                    2),
                (False, Chapter("test", Episode("e1", Scene("1"))),
                    1),
                (False, Episode("test", Scene("1"), Scene("2"), Scene("3")),
                    3),
                (False, Scene("1"), 1),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Counter(v).countScene(), expect)
        validatedTestingWithFail(self, "countScene", _checkcode, data)

    def test_countAction(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("1", Action("a"), Action("a"))))),
                    2),
                (False, Chapter("c1", Episode("e1", Scene("s1", Action("a")))),
                    1),
                (False, Episode("e1", Scene("s1")),
                    0),
                (False, Scene("s1", Action("a")), 1),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Counter(v).countAction(), expect)
        validatedTestingWithFail(self, "countAction", _checkcode, data)

    def test_countCharsOfDirection(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a","apple"))))),
                    5),
                (False, Scene("s1", Action("a","apple"), Action("a","orange")),
                    11),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Counter(v).countCharsOfDirection(), expect)
        validatedTestingWithFail(self, "countCharsOfDirection", _checkcode, data)

    def test_countCharsOfShot(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a",Shot("apple")))))),
                    5),
                (False, Scene("s1", Action("a",Shot("apple"), Shot("orange"))),
                    11),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Counter(v).countCharsOfShot(), expect)
        validatedTestingWithFail(self, "countCharsOfShot", _checkcode, data)

    def test_countAsManupaperRows(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a",Shot("apple"*10)))))),
                    20, 3),
                (False, Scene("s1", Action("a",Shot("apple", isTerm=True), Shot("apple"))),
                    20, 2),
                (False, Scene("s1", Action("a",Shot("apple"), Shot("apple"))),
                    20, 1),
                ]
        def _checkcode(v, c, expect):
            self.assertEqual(Counter(v).countAsManupaperRows(c), expect)
        validatedTestingWithFail(self, "countAsManupaperRows", _checkcode, data)

    def test_countActType(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("a",act_type=ActType.BE))))),
                    ActType.BE, 1),
                ]
        def _checkcode(v, t, expect):
            self.assertEqual(Counter(v).countActType(t), expect)
        validatedTestingWithFail(self, "countActType", _checkcode, data)
