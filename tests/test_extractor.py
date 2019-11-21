# -*- coding: utf-8 -*-
"""Test: extractor.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.action import Action
from builder.chapter import Chapter
from builder.combaction import CombAction
from builder.day import Day
from builder.description import Description, DescType, NoDesc
from builder.episode import Episode
from builder.extractor import Extractor
from builder.flag import Flag, NoDeflag, NoFlag
from builder.person import Person
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story
from builder.time import Time


_FILENAME = "extractor.py"


class ExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Extractor class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")
        self.hana = Person("Hana", "", 15, "female", "girl")

    def test_attributes(self):
        tmp = Extractor(Story("test"))
        self.assertIsInstance(tmp, Extractor)

    def test_chapters(self):
        ch1 = Chapter("apple")
        ch2 = Chapter("orange")
        data = [
                (False, Story("test", ch1, ch2), [ch1, ch2]),
                (False, ch1, [ch1,]),
                (False, Episode("e1",""), []),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).chapters
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "chapters", _checkcode, data)

    def test_episodes(self):
        ep1 = Episode("apple", "an apple")
        ep2 = Episode("orange", "a orange")
        data = [
                (False, Story("test", Chapter("1", ep1, ep2)),
                    [ep1, ep2]),
                (False, Story("test", Chapter("1", ep1), Chapter("2", ep2)),
                    [ep1, ep2]),
                (True, Story("test", Chapter("1", ep1, ep2)),
                    [ep2, ep1]),
                (False, Chapter("1", ep1),
                    [ep1]),
                (False, ep1, [ep1]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).episodes
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "episodes", _checkcode, data)

    def test_scenes(self):
        sc1 = Scene("apple", "an apple")
        sc2 = Scene("orange", "a orange")
        data = [
                (False, Story("test", Chapter("1", Episode("e1", "", sc1, sc2))),
                    [sc1, sc2]),
                (False, Chapter("1", Episode("e1","", sc1)),
                    [sc1]),
                (False, Episode("e1","", sc1),
                    [sc1]),
                (False, sc1, [sc1]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).scenes
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "scenes", _checkcode, data)

    def test_actions(self):
        act1 = Action(self.taro, "apple")
        act2 = Action(self.hana, "orange")
        cmbact1 = CombAction(act1, act2)
        data = [
                (False, Story("test",
                    Chapter("1", Episode("e1","",
                        Scene("s1", "", act1, act2)))),
                    [act1, act2]),
                (False, Story("test",
                    Chapter("1", Episode("e1","",
                        Scene("s1","", cmbact1)))),
                    [act1, act2]),
                (False, Chapter("1", Episode("e1","",
                    Scene("s1","", act1))),
                    [act1]),
                (False, Episode("e1","", Scene("s1","", act1)),
                    [act1]),
                (False, Scene("s1","", act1), [act1]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).actions
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "actions", _checkcode, data)

    def test_outlines(self):
        act1 = Action(self.taro, "apple")
        act2 = Action(self.hana, "orange")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", act1, act2)))),
                    ["apple", "orange"]),
                (False, Scene("s1","", act1, Action("melon")),
                    ["apple", "melon"]),
                (False, Scene("s1",""),
                    []),
                (False, Scene("s1","", Action(self.hana)),
                    []),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).outlines
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "outlines", _checkcode, data)

    def test_descriptions(self):
        act1 = Action(self.taro, "apple")
        act2 = Action(self.hana, "orange")
        d1 = Description("an apple",)
        d2 = Description("a orange",)
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", act1._setDescription(d1, desc_type=DescType.DESC),
                        act2._setDescription(d2, desc_type=DescType.DESC))))),
                    [d1, d2]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).descriptions
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "descriptions", _checkcode, data)

    def test_persons(self):
        act1 = Action(self.taro, "apple")
        act2 = Action(self.hana, "orange")
        data = [
                (False, Story("test",
                    Chapter("1", Episode("e1","",
                        Scene("s1","", act1, act2)))),
                    [self.taro, self.hana]),
                (False, Scene("s1","", act1,act2),
                    [self.taro, self.hana]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).persons
            self.assertIsInstance(tmp, list)
            self.assertEqual(set(tmp), set(expect))
        validated_testing_withfail(self, "persons", _checkcode, data)

    def test_stages(self):
        st1 = Stage("school")
        st2 = Stage("room")
        data = [
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","", stage=st1)))),
                    [st1,]),
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","", stage=st1), Scene("s2", "", stage=st2)))),
                    [st1, st2]),
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","", stage=st1), Scene("s2", "",)))),
                    [st1,]),
                (False, Scene("s1","", stage=st1),
                    [st1,]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).stages
            self.assertIsInstance(tmp, list)
            self.assertEqual(set(tmp), set(expect))
        validated_testing_withfail(self, "stages", _checkcode, data)

    def test_days(self):
        day1 = Day("day1", 1,1,2019)
        day2 = Day("day2", 2,14,2019)
        data = [
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","",day=day1)))),
                    [day1,]),
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","",day=day1), Scene("s2","", day=day2)))),
                    [day1, day2]),
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","",day=day1), Scene("s2","",)))),
                    [day1,]),
                (False, Scene("s1","", day=day1),
                    [day1,]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).days
            self.assertIsInstance(tmp, list)
            self.assertEqual(set(tmp), set(expect))
        validated_testing_withfail(self, "days", _checkcode, data)

    def test_times(self):
        time1 = Time("morning", 8,0)
        time2 = Time("night", 20,0)
        data = [
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","",time=time1)))),
                    [time1,]),
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","",time=time1), Scene("s2","",time=time2)))),
                    [time1, time2]),
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","",time=time1), Scene("s2","")))),
                    [time1,]),
                (False, Scene("s","", time=time1), [time1,]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).times
            self.assertIsInstance(tmp, list)
            self.assertEqual(set(tmp), set(expect))
        validated_testing_withfail(self, "times", _checkcode, data)

    def test_flags(self):
        f1 = Flag("apple")
        f2 = Flag("orange")
        df1 = Flag("melon")
        data = [
                (False, Story("test", Chapter("1", Episode("e1","",
                    Scene("s1","", Action(self.taro).flag(f1))))),
                    [f1,]),
                (False, Scene("s1","",
                    Action(self.taro).flag(f1).deflag(df1)),
                    [f1, df1]),
                (False, Scene("s1","",
                    Action(self.taro).deflag(df1), Action(self.hana).flag(f1)),
                    [f1, df1]),
                ]
        def _checkcode(v, expect):
            tmp = Extractor(v).flags
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "flags", _checkcode, data)
