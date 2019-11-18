# -*- coding: utf-8 -*-
"""Test: parser.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.parser import Parser
from builder.parser import _actionLayersFromAction
from builder.parser import _descriptionConnectedFromAction
from builder.parser import _descriptionsFromAction
from builder.parser import _scenariosFromAction
from builder.parser import _storyFilteredInAction
from builder.parser import _tagActionConverted
from builder.parser import _tagReplacedInDocument
from builder.action import Action, ActType, TagAction, TagType
from builder.combaction import CombAction
from builder.person import Person


_FILENAME = "parser.py"


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Parser class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student", "me:俺")
        self.hana = Person("Hana", "", 15, "female", "girl", "me:私")

    def test_actionLayersFromAction(self):
        act1 = Action(self.taro, layer="test")
        act2 = Action(self.hana, layer="test")
        data = [
                (False, act1, "A",
                    [("test", "A", act1),],),
                (False, CombAction(act1, act2), "B",
                    [("test", "B", act1), ("test", "B", act2)],),
                ]
        def _checkcode(v, h,expect):
            self.assertEqual(_actionLayersFromAction(v, h), expect)
        validated_testing_withfail(self, "actionLayersFromAction", _checkcode, data)

    def test_descriptionConnectedFromAction(self):
        data = [
                (False, Action(self.taro).d("test", "apple"),
                    ("test。apple",),),
                (False, Action(self.taro).d("test"),
                    ("test",),),
                (False, CombAction(Action(self.taro).d("test"), Action(self.taro).d("apple")),
                    [("test",), ("apple",)],),
                ]
        def _checkcode(v, expect):
            if isinstance(v, TagAction):
                self.assertEqual(_descriptionConnectedFromAction(v), v)
            elif isinstance(v, CombAction):
                tmp = _descriptionConnectedFromAction(v)
                self.assertEqual(list(v.description.descs for v in tmp.actions), expect)
            else:
                self.assertEqual(_descriptionConnectedFromAction(v).description.descs,
                        expect)
        validated_testing_withfail(self, "descriptionConnectedFromAction", _checkcode, data)

    def test_descriptionsFromAction(self):
        data = [
                (False, Action(self.taro).d("test"),
                    True, ["　test。"],),
                (False, Action(self.taro).t("test"),
                    True, ["「test」"],),
                (False, CombAction(Action(self.taro).d("test"), Action(self.taro).d("apple"),
                    ),
                    True, ["　test。apple。"],),
                ]
        def _checkcode(v, is_cmt, expect):
            self.assertEqual(_descriptionsFromAction(v, is_cmt), expect)
        validated_testing_withfail(self, "descriptionsFromAction", _checkcode, data)

    @unittest.skip("complex function")
    def test_layerReplacedFrom(self):
        pass

    @unittest.skip("currently no need")
    def test_outlinesFrom(self):
        pass

    @unittest.skip("complex function")
    def test_pronounReplacedInScene(self):
        pass

    def test_scenariosFromAction(self):
        from builder.scene import ScenarioType
        data = [
                (False, Action(self.taro, "test"), False,
                    [(ScenarioType.DIRECTION, "test。")],),
                (False, Action(self.taro, "test", act_type=ActType.TALK), False,
                    [(ScenarioType.DIALOGUE, "Taro「test」")],),
                ]
        def _checkcode(v, is_cmt, expect):
            self.assertEqual(_scenariosFromAction(v, is_cmt), expect)
        validated_testing_withfail(self, "scenariosFromAction", _checkcode, data)

    def test_storyFilteredInAction(self):
        act1 = Action(self.taro)
        act2 = Action(self.hana)
        combact = CombAction(act1, act2)
        data = [
                (False, act1, 1, Action, act1,),
                (False, act1, 9, None, None,),
                (False, combact, 1, CombAction,combact,),
                ]
        def _checkcode(v, pri, cls, expect):
            tmp = _storyFilteredInAction(v, pri)
            if cls:
                self.assertIsInstance(tmp, cls)
            if isinstance(tmp, CombAction):
                self.assertEqual(len(tmp.actions), len(expect.actions))
            elif tmp:
                self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "storyFilteredInAction", _checkcode, data)

    def test_tagActionConverted(self):
        data = [
                (False, TagAction("test", tag_type=TagType.COMMENT), True,
                    "<!--test-->",),
                (False, TagAction("test", tag_type=TagType.COMMENT), False,
                    "",),
                (False, TagAction("test", tag_type=TagType.BR), True,
                    "\n\n",),
                (False, TagAction("test", tag_type=TagType.HR), True,
                    "----"*8,),
                (False, TagAction("test", tag_type=TagType.SYMBOL), True,
                    "\ntest\n",),
                (False, TagAction("test", "1", tag_type=TagType.TITLE), True,
                    "# test",),
                ]
        def _checkcode(v, is_cmt, expect):
            self.assertEqual(_tagActionConverted(v, is_cmt), expect)
        validated_testing_withfail(self, "tagActionConverted", _checkcode, data)

    def test_tagReplacedInDocument(self):
        base_words = {"T":"test"}
        data = [
                (False, self.taro, "$meは$Sだ", base_words, "A",
                    "俺はTaroだ",),
                (True, self.taro, "$meは$Sだ$", base_words, "A",
                    "俺はTaroだ",),
                ]
        def _checkcode(subject, t, words, msg, expect):
            self.assertEqual(_tagReplacedInDocument(subject, t, words, msg), expect)
        validated_testing_withfail(self, "tagReplacedInDocument", _checkcode, data)
