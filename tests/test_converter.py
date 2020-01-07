# -*- coding: utf-8 -*-
"""Test: converter.py
"""
## public libs
import datetime
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.action import Action
from builder.block import Block
from builder.chapter import Chapter
from builder.converter import Converter
from builder.episode import Episode
from builder.extractor import Extractor
from builder.person import Person
from builder.scene import Scene
from builder.story import Story
from builder.pronoun import Who


_FILENAME = "converter.py"


class ConverterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Converter class")

    def setUp(self):
        self.taro = Person("Taro", "", 15, "male", "student", "me:俺")
        self.hana = Person("Hana", "", 20, "female", "OL", "me:わたし")

    def test_attributes(self):
        tmp = Converter()
        self.assertIsInstance(tmp, Converter)

    def test_srcExpandBlocks(self):
        ac1, ac2, ac3 = Action("apple"), Action("orange"), Action("melon")
        bk1, bk2 = Block("A", ac1), Block("B", ac2, ac3)
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", ac1, ac2)))),
                    (ac1, ac2)),
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", bk1, bk2)))),
                    (ac1, ac2, ac3)),
                ]
        def _checkcode(v, expect):
            tmp = Extractor.actionsFrom(Converter.srcExpandBlocks(v))
            self.assertEqual(tmp, expect)
        validatedTestingWithFail(self, "srcExpandBlocks", _checkcode, data)

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
                (False, Story("test", ch1), 5, Story("test",ch1,)),
                (False, Story("test", ch1,ch2), 5, Story("test",ch1,)),
                (False, Chapter("test", ep1), 5, Chapter("test",ep1,)),
                (False, Chapter("test", ep1,ep2), 5, Chapter("test",ep1,)),
                (False, Episode("test", sc1,), 5, Episode("test",sc1,)),
                (False, Episode("test", sc1,sc2), 5, Episode("test",sc1,)),
                (False, Scene("test", act1), 5, Scene("test",act1,)),
                (False, Scene("test", act1,act2), 5, Scene("test",act1,)),
                ]
        def _checkcode(v, pri, expect):
            tmp = Converter.srcFilterByPriority(v, pri)
            self.assertEqual(len(tmp.data), len(expect.data))
        validatedTestingWithFail(self, "srfFilterByPriority", _checkcode, data)

    def test_srcReplacedPronouns(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action(subject=self.taro), Action("apple"))))),
                    [self.taro, self.taro]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor.actionsFrom(Converter.srcReplacedPronouns(v))
            self.assertEqual([v.subject for v in tmp], expect)
        validatedTestingWithFail(self, "srcReplacedPronouns", _checkcode, data)

    def test_srcReplacedTags(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("$Sは$appleを食べた", subject=self.taro))))),
                    {"apple":"林檎"},
                    [("Taroは林檎を食べた",)]),
                ]
        def _checkcode(v, tags, expect):
            tmp = Extractor.actionsFrom(Converter.srcReplacedTags(v, tags, "$"))
            self.assertEqual([v.data for v in tmp], expect)
        validatedTestingWithFail(self, "srcReplacedTags", _checkcode, data)

    def test_srcReducedByChapter(self):
        ch1, ch2 = Chapter("c1"), Chapter("c2")
        data = [
                (False, Story("test", ch1, ch2), 0,2,
                    (ch1, ch2)),
                (False, Story("test", ch1, ch2), 1,1,
                    (ch2,)),
                (False, Story("test", ch1, ch2), 0,-1,
                    (ch1, ch2)),
                ]
        def _checkcode(v, start, end, expect):
            tmp = Converter.srcReducedByChapter(v, start, end)
            self.assertEqual(Extractor.chaptersFrom(tmp), expect)
        validatedTestingWithFail(self, "srcReducedByChapter", _checkcode, data)

    def test_srcReducedByEpisode(self):
        ep1, ep2 = Episode("e1"), Episode("e2")
        data = [
                (False, Story("test", Chapter("c1",ep1), Chapter("c2",ep2)), 0,2,
                    (ep1,ep2)),
                (False, Story("test", Chapter("c1",ep1), Chapter("c2",ep2)), 1,1,
                    (ep2,)),
                (False, Story("test", Chapter("c1",ep1), Chapter("c2",ep2)), 0,-1,
                    (ep1,ep2)),
                ]
        def _checkcode(v, start, end, expect):
            tmp = Converter.srcReducedByEpisode(v, start, end)
            self.assertEqual(Extractor.episodesFrom(tmp), expect)
        validatedTestingWithFail(self, "srcReducedByEpisode", _checkcode, data)
