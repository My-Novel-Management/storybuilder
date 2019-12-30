# -*- coding: utf-8 -*-
"""Test: converter.py
"""
## public libs
import datetime
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
from utils.util_compare import equalsContainerLists
## local files
from builder.action import Action
from builder.converter import Converter
from builder.block import Block
from builder.chapter import Chapter
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene
from builder.story import Story
from builder.who import Who


_FILENAME = "converter.py"


class ConverterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Converter class")

    def setUp(self):
        self.taro = Person("Taro", "", 15, "male", "student", "me:俺")
        self.hana = Person("Hana", "", 20, "female", "OL", "me:わたし")

    def test_attributes(self):
        tmp = Converter(Story("test"))
        self.assertIsInstance(tmp, Converter)

    def test_srcFilterByPriority(self):
        ch1 = Chapter("c1")
        ch2 = Chapter("c2", priority=1)
        ep1 = Episode("e1")
        ep2 = Episode("e2", priority=1)
        sc1 = Scene("sc1")
        sc2 = Scene("sc2", priority=1)
        act1 = Action("a","apple")
        act2 = Action("a","orange", priority=1)
        data = [
                (False, Story("test", ch1), 5, (ch1,)),
                (False, Story("test", ch1,ch2), 5, (ch1,)),
                (False, Chapter("test", ep1), 5, (ep1,)),
                (False, Chapter("test", ep1,ep2), 5, (ep1,)),
                (False, Episode("test", sc1,), 5, (sc1,)),
                (False, Episode("test", sc1,sc2), 5, (sc1,)),
                (False, Scene("test", act1), 5, (act1,)),
                (False, Scene("test", act1,act2), 5, (act1,)),
                ]
        def _checkcode(v, pri, expect):
            tmp = Converter(v).srcFilterByPriority(pri)
            self.assertTrue(equalsContainerLists(tmp.data[0], expect))
        validatedTestingWithFail(self, "srfFilterByPriority", _checkcode, data)

    def test_srcReplacedPronouns(self):
        ch1 = Chapter("c1")
        data = [
                (False, Story("test", ch1), (ch1,)),
                ]
        def _checkcode(v, expect):
            tmp = Converter(v).srcReplacedPronouns()
            self.assertTrue(equalsContainerLists(tmp.data[0], expect))
        validatedTestingWithFail(self, "srcReplacedPronouns", _checkcode, data)

    def test_srcReplacedPronouns_checkSubject(self):
        act1 = Action("a", "apple", subject=self.taro)
        act2 = Action("a", "orange")
        data = [
                (False, Scene("test", act1, act2),
                    (self.taro, self.taro)),
                ]
        def _checkcode(v, expects):
            tmp = Converter(v).srcReplacedPronouns()
            self.assertEqual(tuple([v.subject for v in tmp.data[0]]),
                    expects)
        validatedTestingWithFail(self, "srcReplacedPronouns_checkSubject",
                _checkcode, data)

    def test_srcReplacedTags(self):
        ch1 = Chapter("c1")
        data = [
                (False, Story("test", ch1),
                    {"M":"俺","S":"太郎"}, "$",
                    (ch1,)),
                ]
        def _checkcode(v, tags, prefix, expect):
            tmp = Converter(v).srcReplacedTags(tags, prefix)
            self.assertTrue(equalsContainerLists(tmp.data[0], expect))
        validatedTestingWithFail(self, "srcReplacedTags", _checkcode, data)

    def test_srcReplacedTags_checkTags(self):
        data = [
                (False, Scene("test", Action("a","$tes食べた", subject=self.taro),
                    camera=self.taro),
                    {"tes":"apple"}, "$",
                    (("apple食べた",),)),
                (False, Scene("test", Action("a","$me食べた", subject=self.taro),
                    camera=self.taro),
                    {"tes":"apple"}, "$",
                    (("俺食べた",),)),
                (False, Scene("test", Action("a","$CM食べた", subject=self.taro),
                    camera=self.hana),
                    {"tes":"apple"}, "$",
                    (("わたし食べた",),)),
                ]
        def _checkcode(v, tags, prefix, expects):
            tmp = Converter(v).srcReplacedTags(tags, prefix)
            self.assertEqual(tuple([v.acts for v in tmp.data[0]]),
                    expects)
        validatedTestingWithFail(self, "srcReplacedTags_checkTags", _checkcode, data)

    def test_srcSerialized(self):
        ch1 = Chapter("c1")
        act1, act2 = Action("a","apple"), Action("a","orange")
        blk1 = Block("b1", act1, act2)
        data = [
                (False, Story("test", ch1), (ch1,)),
                (False, Scene("sc1", act1), (act1,)),
                (False, Scene("sc1", blk1), (act1, act2)),
                ]
        def _checkcode(v, expect):
            tmp = Converter(v).srcSerialized()
            self.assertTrue(equalsContainerLists(tmp.data[0], expect))
        validatedTestingWithFail(self, "srcSerialized", _checkcode, data)

    def test_personNamesConstructed(self):
        data = [
                (False, Person("Taro", "山田,太郎", 15, "male", "job"),
                    ("山田", "太郎", "山田太郎", "太郎・山田")),
                ]
        def _checkcode(v, expects):
            self.assertEqual(Converter.personNamesConstructed(v), expects)
        validatedTestingWithFail(self, "personNamesConstructed", _checkcode, data)
