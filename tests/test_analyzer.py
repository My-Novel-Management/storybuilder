# -*- coding: utf-8 -*-
"""Test: analyzer.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.analyzer import Analyzer, int_ceiled
from builder.action import Action, ActType, TagAction, TagType
from builder.person import Person
from builder.chapter import Chapter
from builder.combaction import CombAction
from builder.episode import Episode
from builder.flag import Flag
from builder.scene import Scene
from builder.story import Story


_FILENAME = "analyzer.py"


class AnalyzerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Analyzer class")

    def setUp(self):
        self.az = Analyzer("")
        self.taro = Person("Taro", "", 17, "male", "student")
        self.hana = Person("Hana", "", 15, "female", "cafe-part")

    def test_attributes(self):
        from MeCab import Tagger
        tmp = Analyzer("")
        self.assertIsInstance(tmp, Analyzer)
        self.assertIsInstance(tmp.tokenizer, Tagger)

    ## base methods
    def test_actionsCount(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro))))),
                    1),
                ]
        def _checkcode(v, expect):
            self.assertEqual(self.az.actionsCount(v), expect)
        validated_testing_withfail(self, "actionsCount", _checkcode, data)

    def test_acttypeCount(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, act_type=ActType.BE))))),
                    ActType.BE, 1),
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, act_type=ActType.BE))))),
                    ActType.ACT, 0),
                ]
        def _checkcode(v, atype, expect):
            self.assertEqual(self.az.acttypeCount(v, atype), expect)
        validated_testing_withfail(self, "acttypeCount", _checkcode, data)

    def test_actTypesCountsFrom(self):
        basedict = dict([(v, 0) for v in ActType])
        def upDict(base: dict, key, val):
            return {**base, **{key:val}}
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, act_type=ActType.BE))))),
                    upDict(basedict, ActType.BE, 1)),
                (False, Scene("s1","",
                        Action(self.taro, act_type=ActType.BE),
                        Action(self.taro, act_type=ActType.BE)),
                    upDict(basedict, ActType.BE, 2)),
                ]
        def _checkcode(v, expect):
            self.assertEqual(self.az.actTypesCountsFrom(v), expect)
        validated_testing_withfail(self, "actTypesCountsFrom", _checkcode, data)

    def test_descsContainsWord(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro).d("apple"))))),
                    "apple", True),
                ]
        def _checkcode(v, w, expect):
            self.assertEqual(self.az.descsContainsWord(v, w), expect)
        validated_testing_withfail(self, "descsContainsWord", _checkcode, data)

    def test_descsManupaperRowCount(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro).d("あ"*25))))),
                    20, 2),
                ]
        def _checkcode(v, c, expect):
            self.assertEqual(self.az.descsManupaperRowCount(v, c), expect)
        validated_testing_withfail(self, "descsManupaperRowCount", _checkcode, data)

    def test_descriptionsCount(self):
        az = Analyzer("")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test").d("apple"))))),
                    6),
                (False, Scene("s1","",
                    Action(self.taro).t("apple")),
                    7),
                ]
        def _checkcode(v, expect):
            self.assertEqual(az.descriptionsCount(v), expect)
        validated_testing_withfail(self, "descriptionsCount", _checkcode, data)

    def test_dialoguesCount(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro).t("apple"))))),
                    self.taro, 1),
                ]
        def _checkcode(v, p, expect):
            self.assertEqual(self.az.dialoguesCount(v, p), expect)
        validated_testing_withfail(self, "dialoguesCount", _checkcode, data)

    def test_dialoguesOfPerson(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro).t("test"))))),
                    self.taro, "test",),
                (False, Scene("s1","",
                    Action(self.taro)),
                    self.taro, []),
                ]
        def _checkcode(v, p, expect):
            tmp = self.az.dialoguesOfPerson(v, p)
            if tmp:
                self.assertEqual(tmp[0][1], expect)
            else:
                self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "dialoguesOfPerson", _checkcode, data)

    def test_flagsCount(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro).flag("1"))))),
                    1),
                (False, Scene("s1","",
                    Action(self.taro).flag("1"), Action(self.hana).deflag("2")),
                    2),
                ]
        def _checkcode(v, expect):
            self.assertEqual(self.az.flagsCount(v), expect)
        validated_testing_withfail(self, "flagsCount", _checkcode, data)

    def test_flagsFrom(self):
        f1 = Flag("1")
        df1 = Flag("1", True)
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro).flag(f1))))),
                    [f1]),
                (False, Scene("s1","",
                    Action(self.taro), Action(self.hana).deflag(df1)),
                    [df1,]),
                (False, Scene("s1","",
                    Action(self.taro).flag(f1), Action(self.hana).deflag(df1)),
                    [f1,df1,]),
                ]
        def _checkcode(v, expect):
            self.assertEqual(self.az.flagsFrom(v), expect)
        validated_testing_withfail(self, "flagsFrom", _checkcode, data)

    def test_generateGramPartWordsCount(self):
        from collections import Counter
        data = [
                (False, Story("test", Chapter("c1", Episode("e1", "",
                    Scene("s1", "",
                        Action(self.taro).d("太郎は話す"))))),
                    "名詞", "",
                    Counter({"太郎":1})),
                (False, Scene("s1","",
                    Action(self.taro).d("太郎は笑う"),
                    Action(self.hana).d("花子は太郎に花を投げた")),
                    "名詞", "人名",
                    Counter({"太郎":2,"花子":1})),
                ]
        def _checkcode(v, gram, sub, expect):
            self.assertEqual(self.az.generateGramPartWordsCount(v, gram, sub), expect)
        validated_testing_withfail(self, "generateGramPartWordsCount", _checkcode, data)

    def test_outlineContainsWord(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "apple"))))),
                    "ap", True),
                ]
        def _checkcode(v, w, expect):
            self.assertEqual(self.az.outlineContainsWord(v, w), expect)
        validated_testing_withfail(self, "outlineContainsWord", _checkcode, data)

    def test_outlinesCount(self):
        az = Analyzer("")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test").d("apple"))))),
                    4),
                ]
        def _checkcode(v, expect):
            self.assertEqual(az.outlinesCount(v), expect)
        validated_testing_withfail(self, "outlinescount", _checkcode, data)

    def test_outlinesManupaperRowCount(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "あ"*21))))),
                    20, 2),
                ]
        def _checkcode(v, c, expect):
            self.assertEqual(self.az.outlinesManupaperRowCount(v, c), expect)
        validated_testing_withfail(self, "outlinesManupaperRowCount", _checkcode, data)

    def test_personsFrom(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro))))),
                    [self.taro,]),
                (False, Scene("s1","",
                    Action(self.taro), Action(self.taro)),
                    [self.taro,]),
                (False, Scene("s1","",
                    Action(self.hana), Action(self.taro)),
                    [self.hana, self.taro]),
                ]
        def _checkcode(v, expect):
            self.assertEqual(self.az.personsFrom(v), expect)
        validated_testing_withfail(self, "personsFrom", _checkcode, data)
