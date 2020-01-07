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
from builder.story import Story


_FILENAME = "counter.py"


class CounterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Counter class")

    def setUp(self):
        self.taro = Person("太郎", "", 15, "male", "student", "me:俺")
        self.basedata = Story("test", Chapter("c1", Episode("e1",
            Scene("s1", Action("apple", subject=self.taro)))))

    def test_attributes(self):
        tmp = Counter()
        self.assertIsInstance(tmp, Counter)

    def test_actions(self):
        data = [
                (False, self.basedata, 1),
                ]
        validatedTestingWithFail(self, "actions", lambda v,expect: self.assertEqual(
            Counter.actions(v), expect), data)

    def test_actType(self):
        data = [
                (False, self.basedata, ActType.ACT, 1),
                (False, self.basedata, ActType.BE, 0),
                ]
        validatedTestingWithFail(self, "actType", lambda v,t,expect: self.assertEqual(
            Counter.actType(v, t), expect), data)

    def test_chapters(self):
        data = [
                (False, self.basedata, 1),
                ]
        validatedTestingWithFail(self, "chapters", lambda v,expect: self.assertEqual(
            Counter.chapters(v), expect), data)

    def test_episodes(self):
        data = [
                (False, self.basedata, 1),
                ]
        validatedTestingWithFail(self, "episodes", lambda v,expect: self.assertEqual(
            Counter.episodes(v), expect), data)

    def test_scenes(self):
        data = [
                (False, self.basedata, 1),
                ]
        validatedTestingWithFail(self, "scenes", lambda v,expect: self.assertEqual(
            Counter.scenes(v), expect), data)

    def test_descriptions(self):
        data = [
                (False, self.basedata, 7),
                ]
        validatedTestingWithFail(self, "descriptions", lambda v,expect: self.assertEqual(
            Counter.descriptions(v), expect), data)

    def test_kanjis(self):
        data = [
                (False, self.basedata, 0),
                (False, Action("太郎は大半食べる"), 5),
                ]
        validatedTestingWithFail(self, "kanjis", lambda v,expect: self.assertEqual(
            Counter.kanjis(v), expect), data)

    def test_manupaperRows(self):
        data = [
                (False, self.basedata, 20, 1),
                ]
        validatedTestingWithFail(self, "manupaperRows", lambda v,c,expect: self.assertEqual(
            Counter.manupaperRows(v, c), expect), data)
