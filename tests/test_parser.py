# -*- coding: utf-8 -*-
"""Test: parser.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.parser import Parser
from builder.action import Action, ActType, TagAction, TagType
from builder.chapter import Chapter
from builder.combaction import CombAction
from builder.day import Day
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene, ScenarioType
from builder.stage import Stage
from builder.story import Story
from builder.time import Time


_FILENAME = "parser.py"


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Parser class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student", "me:俺")
        self.hana = Person("Hana", "", 15, "female", "flowerlist")

    def test_toDescriptions(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", Action(self.taro, "I'm").d("wanna eat"))))),
                    False,
                    ["# test",
                        "## c1", "### e1",
                        "**s1**", "　wanna eat。"]),
                ]
        def _checkcode(v, isCmt, expect):
            tmp = Parser(v).toDescriptions(isCmt)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toDescriptions", _checkcode, data)

    def test_toDescriptionsAsLayer(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", "",
                    Scene("s1","", Action(self.taro, layer="t1").d("apple"),
                        Action(self.hana, layer="t2").d("orange"))))),
                    [("__TITLE__", "# test"),
                        ("c1-e1-s1:t1", "　apple。"),
                        ("c1-e1-s1:t2", "　orange。")]),
                ]
        def _checkcode(v, expect):
            tmp = Parser(v).toDescriptionsAsLayer()
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toDescriptionsAsLayer", _checkcode, data)

    def test_toOutlines(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", "a episode",
                    Scene("s1", "a scene", Action(self.taro, "eat an apple"))))),
                    ["# test",
                        "## c1", "### e1", "a episode",
                        "**s1**", "a scene"]),
                ]
        def _checkcode(v, expect):
            tmp = Parser(v).toOutlines()
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toOutlines", _checkcode, data)

    def test_toOutlinesAsLayer(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", Action(self.taro, "apple", layer="t1"),
                        Action(self.taro, "orange", layer="t2"))))),
                    [("__TITLE__", "# test"),
                        ("c1-e1-s1:t1", "apple"),
                        ("c1-e1-s1:t2", "orange"),]),
                ]
        def _checkcode(v, expect):
            tmp = Parser(v).toOutlinesAsLayer()
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toOutlinesAsLayer", _checkcode, data)

    def test_toScenarios(self):
        time1 = Time("朝", 8,00)
        day1 = Day("ある日", 4,10,2019)
        stage1 = Stage("教室",)
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", "",
                    Scene("s1","", Action(self.taro, "apple"),
                        Action(self.hana, "orange", act_type=ActType.TALK),
                        camera=self.taro, stage=stage1, day=day1, time=time1)))),
                    [(ScenarioType.TITLE, "# test"),
                        (ScenarioType.TITLE, "## c1"),
                        (ScenarioType.TITLE, "### e1"),
                        (ScenarioType.TITLE, "**s1**"),
                        (ScenarioType.PILLAR, "教室:ある日:朝"),
                        (ScenarioType.DIRECTION, "apple"),
                        (ScenarioType.DIALOGUE, "Hana:orange")]),
                ]
        def _checkcode(v, expect):
            tmp = Parser(v).toScenarios()
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toScenarios", _checkcode, data)

    def test_toScenariosAsLayer(self):
        time1 = Time("朝", 8,00)
        day1 = Day("ある日", 4,10,2019)
        stage1 = Stage("教室",)
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", "",
                    Scene("s1","", Action(self.taro, "apple", layer="t1"),
                        Action(self.hana, "orange", act_type=ActType.TALK, layer="t2"),
                        camera=self.taro, stage=stage1, day=day1, time=time1)))),
                    [("__TITLE__", "", ScenarioType.TITLE, "# test"),
                        ("c1-e1-s1:t1", "教室:ある日:朝", ScenarioType.DIRECTION, "apple"),
                        ("c1-e1-s1:t2", "教室:ある日:朝", ScenarioType.DIALOGUE, "Hana:orange")]),
                ]
        def _checkcode(v, expect):
            tmp = Parser(v).toScenariosAsLayer()
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toScenariosAsLayer", _checkcode, data)
