# -*- coding: utf-8 -*-
"""Test: converter.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import __DEF_LAYER__
from builder.action import Action, ActType, TagAction, TagType
from builder.basesubject import NoSubject
from builder.chapter import Chapter
from builder.combaction import CombAction
from builder.converter import Converter
from builder.converter import toConvertTagAction
from builder.episode import Episode
from builder.extractor import Extractor
from builder.person import Person
from builder.scene import Scene
from builder.story import Story
from builder.who import Who


_FILENAME = "converter.py"


class ConverterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Converter class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student", "me:俺")
        self.hana = Person("Hana", "", 15, "female", "flowerist")

    def test_attributes(self):
        data = [
                (False, Story("test",)),
                ]
        def _checkcode(v):
            tmp = Converter(v)
            self.assertIsInstance(tmp, Converter)
        validated_testing_withfail(self, "class", _checkcode, data)

    def test_toFilter(self):
        ch1 = Chapter("c1")
        ch2 = Chapter("c2")
        ep1 = Episode("e1", "")
        ep2 = Episode("e2", "")
        sc1, sc2 = Scene("s1",""), Scene("s2","")
        data = [
                (False, Story("test", ch1, ch2.setPriority(1)),
                    5, "chapter", 1,),
                (False, Chapter("c1", ep1, ep2.setPriority(1)),
                    5, "episode", 1),
                (False, Episode("e1","", sc1, sc2.setPriority(1)),
                    5, "scene", 1),
                (True, Action(self.taro, "").setPriority(1),
                    5, "action", 1),
                ]
        def _checkcode(v, pri, isWhat, expect):
            tmp = Converter(v).toFilter(pri)
            if isWhat == 'chapter':
                self.assertEqual(len(Extractor(tmp).chapters), expect)
            elif isWhat == 'episode':
                self.assertEqual(len(Extractor(tmp).episodes), expect)
            elif isWhat == 'scene':
                self.assertEqual(len(Extractor(tmp).scenes), expect)
            elif isWhat == 'action':
                self.assertEqual(len(Extractor(tmp).actions), expect)
        validated_testing_withfail(self, "toFilter", _checkcode, data)

    def test_toLayer(self):
        lay0 = TagAction(__DEF_LAYER__, tag_type=TagType.SET_LAYER)
        lay1 = TagAction("test1", tag_type=TagType.SET_LAYER)
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro),
                        lay1, Action(self.taro)))))),
                (False, Chapter("c1", Episode("e1","",
                    Scene("s1","", lay1, Action(self.taro, layer="test2"),),
                    Scene("s2","", Action(self.taro))))),
                (False, Episode("e1","",
                    Scene("s1","", lay1, Action(self.taro),
                        lay0, Action(self.taro)))),
                ]
        def _checkcode(v):
            tmp = Converter(v).toLayer()
            tmp1 = Extractor(tmp).actions
            for v in tmp1:
                self.assertTrue(v.layer != __DEF_LAYER__)
        validated_testing_withfail(self, "toLayer", _checkcode, data)

    def test_toReplacePronoun(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", Action(self.taro), Action("食べる"))))),
                    self.taro,),
                (True, Scene("s1","", Action("test"), Action("eat")),
                    NoSubject()),
                (True, Episode("e1","",
                    Scene("s1","", Action(self.hana), Action("eat")),
                    Scene("s2","", Action(self.taro), Action("eat"))),
                    self.hana,),
                ]
        def _checkcode(v, expect):
            base = Extractor(v).actions
            self.assertIsInstance(base[1].subject, Who)
            tmp = Converter(v).toReplacePronoun()
            tmp1 = Extractor(tmp).actions
            for v in tmp1[1:]:
                self.assertEqual(v.subject, expect)
        validated_testing_withfail(self, "toReplacePronoun", _checkcode, data)

    def test_toConnectDescriptions(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", Action(self.taro).d("test","apple"))))),
                    [("test。apple",)]),
                (False, Scene("s1","", Action(self.taro).d("test",),
                    Action(self.taro).d("apple","orange")),
                    [("test",),("apple。orange",)]),
                ]
        def _checkcode(v, expects):
            tmp = Converter(v).toConnectDescriptions()
            tmp1 = Extractor(tmp).actions
            for v, exp in zip(tmp1, expects):
                self.assertEqual(v.description.descs, exp)
        validated_testing_withfail(self, "toConnectDescriptions", _checkcode, data)

    def test_toReplaceTag(self):
        words = {"apple":"林檎", "orange":"蜜柑"}
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","", Action(self.taro, "$Sは食べる").d("$Mのものだ"))))),
                    words,
                    ["Taroは食べる",], [("俺のものだ",),]),
                (False, Scene("s1","", Action(self.taro, "$appleを食べる").d("$orangeを食べる"),),
                    words,
                    ["林檎を食べる",], [("蜜柑を食べる",),]),
                ]
        def _checkcode(v, words, expects1, expects2):
            tmp = Converter(v).toReplaceTag(words)
            tmp1 = Extractor(tmp).actions
            for v, exp_out, exp_desc in zip(tmp1, expects1, expects2):
                self.assertEqual(v.outline, exp_out)
                self.assertEqual(v.description.descs, exp_desc)
        validated_testing_withfail(self, "toReplaceTag", _checkcode, data)

    def test_toConveretTagAction(self):
        data = [
                (False, TagAction("test", tag_type=TagType.COMMENT),
                    True, "<!--test-->"),
                (False, TagAction("test", tag_type=TagType.BR),
                    True, "\n\n"),
                (False, TagAction("test", tag_type=TagType.HR),
                    True, "--------"*8,),
                (False, TagAction("test", tag_type=TagType.SYMBOL),
                    True, "\ntest\n"),
                (False, TagAction("test", "2", tag_type=TagType.TITLE),
                    True, "\n## test\n"),
                ]
        def _checkcode(v, isCmt, expect):
            tmp = toConvertTagAction(v, isCmt)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toConvertTagAction", _checkcode, data)
