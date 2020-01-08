# -*- coding: utf-8 -*-
"""Test: extractor.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local file_
from builder.action import Action
from builder.chapter import Chapter
from builder.day import Day
from builder.episode import Episode
from builder.extractor import Extractor
from builder.item import Item
from builder.person import Person
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word


_FILENAME = "extractor.py"


class ExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Extractor class")

    def setUp(self):
        self.taro = Person("太郎", "", 15, (1,1), "male", "student")

    def _getStory(self, act: Action):
        return Story("test", Chapter("c1", Episode("e1",
            Scene("s1", act))))

    def test_attributes(self):
        tmp = Extractor()
        self.assertIsInstance(tmp, Extractor)

    def test_storyFrom(self):
        s1 = Story("test")
        data = [
                (False, s1, s1),
                (True, Chapter("1"), 1),
                ]
        validatedTestingWithFail(self, "storyFrom", lambda v, expect: self.assertEqual(
            Extractor.storyFrom(v), expect), data)

    def test_chaptersFrom(self):
        ch1, ch2 = Chapter("1"), Chapter("2")
        data = [
                (False, Story("test", ch1, ch2), (ch1, ch2)),
                (False, Story("test"), ()),
                (False, ch1, (ch1,)),
                (True, Episode("e1"), ()),
                (True, Scene("s1"), ()),
                ]
        validatedTestingWithFail(self, "chaptersFrom", lambda v, expect: self.assertEqual(
            Extractor.chaptersFrom(v), expect), data)

    def test_episodesFrom(self):
        ep1, ep2 = Episode("1"), Episode("2")
        data = [
                (False, Story("test", Chapter("c1", ep1, ep2)),
                    (ep1, ep2)),
                (False, Story("test", Chapter("c1", ep1), Chapter("c2", ep2)),
                    (ep1, ep2)),
                (False, Chapter("c1", ep1), (ep1,)),
                (False, ep1, (ep1,)),
                (True, Scene("s1"), ()),
                ]
        validatedTestingWithFail(self, "episodesFrom", lambda v, expect: self.assertEqual(
            Extractor.episodesFrom(v), expect), data)

    def test_scenesFrom(self):
        sc1, sc2 = Scene("s1"), Scene("s2")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", sc1, sc2))),
                    (sc1, sc2)),
                (False, Chapter("c1", Episode("e1", sc1), Episode("e2", sc2)),
                    (sc1, sc2)),
                ]
        validatedTestingWithFail(self, "scenesFrom", lambda v, expect: self.assertEqual(
            Extractor.scenesFrom(v), expect), data)

    def test_actionsFrom(self):
        ac1, ac2 = Action("a"), Action("b")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", ac1, ac2)))),
                    (ac1, ac2)),
                (False, Episode("e1", Scene("s1", ac1), Scene("s2", ac2)),
                    (ac1, ac2)),
                ]
        validatedTestingWithFail(self, "actionsFrom", lambda v, expect: self.assertEqual(
            Extractor.actionsFrom(v), expect), data)

    def test_directionsFrom(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("apple", "orange"))))),
                    ("apple", "orange")),
                ]
        validatedTestingWithFail(self, "directionsFrom", lambda v, expect: self.assertEqual(
            Extractor.directionsFrom(v), expect), data)

    def test_daysFrom(self):
        dy1 = Day("apple", 1,1,2020)
        data = [
                (False, self._getStory(Action(dy1)), (dy1,)),
                ]
        validatedTestingWithFail(self, "daysFrom", lambda v,expect: self.assertEqual(
            Extractor.daysFrom(v), expect), data)

    def test_itemsFrom(self):
        it1 = Item("apple")
        data = [
                (False, self._getStory(Action(it1)), (it1,)),
                ]
        validatedTestingWithFail(self, "itemsFrom", lambda v,expect: self.assertEqual(
            Extractor.itemsFrom(v), expect), data)

    def test_objectsFrom(self):
        dy1 = Day("apple", 1,1,2020)
        it1 = Item("orange")
        wd1 = Word("melon")
        data = [
                (False, self._getStory(Action(dy1,it1,wd1)), (dy1,it1,wd1)),
                ]
        validatedTestingWithFail(self, "objectsFrom", lambda v,expect: self.assertEqual(
            Extractor.objectsFrom(v), expect), data)

    def test_personsFrom(self):
        data = [
                (False, self._getStory(Action(self.taro)), (self.taro,)),
                ]
        validatedTestingWithFail(self, "personsFrom", lambda v,expect: self.assertEqual(
            Extractor.personsFrom(v), expect), data)

    def test_stagesFrom(self):
        st1 = Stage("apple")
        data = [
                (False, self._getStory(Action(st1)), (st1,)),
                ]
        validatedTestingWithFail(self, "stagesFrom", lambda v,expect: self.assertEqual(
            Extractor.stagesFrom(v), expect), data)

    def test_subjectsFrom(self):
        data = [
                (False, self._getStory(Action(subject=self.taro)), (self.taro,)),
                ]
        validatedTestingWithFail(self, "subjectsFrom", lambda v,expect: self.assertEqual(
            Extractor.subjectsFrom(v), expect), data)

    def test_timesFrom(self):
        tm1 = Time("apple", 12,0,0)
        data = [
                (False, self._getStory(Action(tm1)), (tm1,)),
                ]
        validatedTestingWithFail(self, "timesFrom", lambda v,expect: self.assertEqual(
            Extractor.timesFrom(v), expect), data)

    def test_wordsFrom(self):
        wd1 = Word("apple")
        data = [
                (False, self._getStory(Action(wd1)), (wd1,)),
                ]
        validatedTestingWithFail(self, "wordsFrom", lambda v,expect: self.assertEqual(
            Extractor.wordsFrom(v), expect), data)
