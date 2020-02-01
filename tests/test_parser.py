# -*- coding: utf-8 -*-
"""Test: parser.py
"""
## public libs
import unittest
import datetime
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType, DataType
from builder import ConteData
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.parser import Parser
from builder.person import Person
from builder.pronoun import When
from builder.rubi import Rubi
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story


_FILENAME = "parser.py"


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Parser class")

    def setUp(self):
        self.taro = Person("太郎", "", 15, (1,1), "male", "student", "me:俺")
        self.hana = Person("花子", "", 15, (1,1), "female", "student", "me:私")
        self.room = Stage("部屋")

    def test_attributes(self):
        tmp = Parser()
        self.assertIsInstance(tmp, Parser)

    def test_toContes(self):
        self.hana.setTexture("金髪ロング")
        self.room.setTexture("ひび割れ")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("apple", subject=self.taro))))),
                    ((DataType.STORY_TITLE, "test"),
                        (DataType.CHAPTER_TITLE, "c1"),
                        (DataType.EPISODE_TITLE, "e1"),
                        (DataType.SCENE_TITLE, "s1 [6]c"),
                        (DataType.SCENE_SETTING,
                            {"camera":"__who__",
                                "area":"__where__",
                                "stage":"__where__",
                                "day":When().data,
                                "week":When().data.weekday(),
                                "time":"__when__"}),
                        (DataType.ACTION,
                            ConteData(ActType.ACT,
                                "", "太郎", (), "apple", 0, "")),
                        (DataType.DATA_LIST, ["太郎"]),
                        (DataType.DATA_LIST, []),
                            )),
                (False, Scene("s1",
                    Action("apple", subject=self.taro, act_type=ActType.TALK)),
                    ((DataType.SCENE_TITLE, "s1 [7]c"),
                        (DataType.SCENE_SETTING,
                            {"camera":"__who__",
                                "area":"__where__",
                                "stage":"__where__",
                                "day":When().data,
                                "week":When().data.weekday(),
                                "time":"__when__"}),
                        (DataType.ACTION,
                            ConteData(ActType.TALK,
                                "apple", "太郎", (), "", 0, "")),
                        (DataType.DATA_LIST, ["太郎"]),
                        (DataType.DATA_LIST, []),
                            )),
                (False, Scene("s1",
                    Action("apple", subject=self.hana),
                    camera=self.taro, stage=self.room),
                    ((DataType.SCENE_TITLE, "s1 [6]c"),
                        (DataType.SCENE_SETTING,
                            {"camera":"太郎",
                                "area":"__where__",
                                "stage":"部屋",
                                "day":When().data,
                                "week":When().data.weekday(),
                                "time":"__when__"}),
                        (DataType.STAGE_SETTING, {"name":"部屋","texture":"ひび割れ"}),
                        (DataType.PERSON_SETTING, {"name":"花子","texture":"金髪ロング"}),
                        (DataType.ACTION,
                            ConteData(ActType.ACT, "", "花子", (),"apple", 0, "")),
                        (DataType.DATA_LIST, ["花子"]),
                        (DataType.DATA_LIST, []),
                        )),
                (False, Scene("s1",
                    Action("apple", "#orange", subject=self.taro)),
                    ((DataType.SCENE_TITLE, "s1 [13]c"),
                        (DataType.SCENE_SETTING,
                            {"camera":"__who__",
                                "area":"__where__",
                                "stage":"__where__",
                                "day":When().data,
                                "week":When().data.weekday(),
                                "time":"__when__"}),
                        (DataType.ACTION,
                            ConteData(ActType.ACT,
                                "", "太郎", (), "＃orange", 0, "")),
                        (DataType.DATA_LIST, ["太郎"]),
                        (DataType.DATA_LIST, []),
                            )),
                ]
        def _checkcode(v, expect):
            tmp = Parser.toContes(v)
            self.assertEqual(tmp, expect)
        validatedTestingWithFail(self, "toContes", _checkcode, data)

    def test_toDescriptions(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("apple"))))),
                    ((DataType.STORY_TITLE, "test"),
                        (DataType.CHAPTER_TITLE, "c1"),
                        (DataType.EPISODE_TITLE, "e1 [6]c"),
                        (DataType.SCENE_TITLE, "s1 [6]c"),
                        (DataType.DESCRIPTION, "apple。"))),
                (False, Scene("s1", Action("apple", "&"), Action("orange")),
                    ((DataType.SCENE_TITLE, "s1 [14]c"),
                        (DataType.DESCRIPTION, "apple。orange。"))),
                (False, Scene("s1", Action("apple", "&", act_type=ActType.TALK),
                    Action("orange")),
                    ((DataType.SCENE_TITLE, "s1 [15]c"),
                        (DataType.DIALOGUE, "apple。orange。"))),
                ]
        def _checkcode(v, expect):
            tmp = Parser.toDescriptions(v)
            self.assertEqual(tmp, expect)
        validatedTestingWithFail(self, "toDescriptions", _checkcode, data)

    def test_toDescriptionsWithRubi(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1",
                        Action("小太郎と一緒に"),
                        Action("太郎の野郎"),
                        )))),
                    {"太郎":Rubi("太郎","｜太郎《たろう》", ("小太郎",))},
                    ((DataType.STORY_TITLE, "test"),
                        (DataType.CHAPTER_TITLE, "c1"),
                        (DataType.EPISODE_TITLE, "e1 [15]c"),
                        (DataType.SCENE_TITLE, "s1 [15]c"),
                        (DataType.DESCRIPTION, "小太郎と一緒に。"),
                        (DataType.DESCRIPTION, "｜太郎《たろう》の野郎。"),
                        )),
                ]
        def _checkcode(v, rubis, expect):
            tmp = Parser.toDescriptionsWithRubi(v, rubis)
            self.assertEqual(tmp, expect)
        validatedTestingWithFail(self, "toDescriptionsWithRubi", _checkcode, data)

    ## methods (for parts)
    def test_descFrom(self):
        data = [
                (False, Action("apple", "orange"),
                    "apple。orange。"),
                (False, Action("apple", "orange", act_type=ActType.TALK),
                    "apple。orange"),
                (False, Action("apple", "orange", act_type=ActType.VOICE),
                    "apple。orange"),
                ]
        validatedTestingWithFail(self, "descFrom", lambda v, expect: self.assertEqual(
            Parser.descFrom(v), expect), data)
