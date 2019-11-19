# -*- coding: utf-8 -*-
"""Test: analyzer.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.analyzer import Analyzer, int_ceiled
from builder.analyzer import _acttypeCountsInAction
from builder.analyzer import _containsWordIn
from builder.analyzer import _containsWordInAction
from builder.analyzer import _descriptionCountInAction
from builder.analyzer import _descriptionManupaperCountsInAction
from builder.analyzer import _dialogueCountInAction
from builder.analyzer import _dialoguesOfPersonInAction
from builder.analyzer import _flagsInAction
from builder.analyzer import _outlineCountsInAction
from builder.analyzer import _outlineManupaperCountsInAction
from builder.analyzer import _personsInAction
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
        self.taro = Person("Taro", "", 17, "male", "student")
        self.hana = Person("Hana", "", 15, "female", "cafe-part")

    def test_attributes(self):
        from MeCab import Tagger
        tmp = Analyzer("")
        self.assertIsInstance(tmp, Analyzer)
        self.assertIsInstance(tmp.tokenizer, Tagger)

    ## methods
    def test_containsWord(self):
        az = Analyzer("")
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test"))))),
                    "test", True),
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test").d("apple"))))),
                    ("test", "apple"), True),
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test").d("apple"))))),
                    ("test", "orrange"), False),
                ]
        def _checkcode(v, t, expect):
            self.assertEqual(az.containsWord(v, t), expect)
        validated_testing_withfail(self, "containsWord", _checkcode, data)

    ## functions
    def test_acttypeCountsInAction(self):
        data = [
                (False, Action(self.taro, act_type=ActType.ACT), ActType.ACT, 1,),
                (False, Action(self.taro, act_type=ActType.BE), ActType.ACT, 0,),
                (False, CombAction(Action(self.taro, act_type=ActType.ACT), Action(self.taro, act_type=ActType.ACT)),
                    ActType.ACT, 2,),
                (False, TagAction("", tag_type=TagType.COMMENT), ActType.ACT, 0,),
                ]
        def _checkcode(v, atype, expect):
            self.assertEqual(_acttypeCountsInAction(v, atype), expect)
        validated_testing_withfail(self, "acttypeCountsInAction", _checkcode, data)

    def test_containsWordIn(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test"))))),
                    "test", True),
                (False, Story("test", Chapter("c1", Episode("e1","",
                    Scene("s1","",
                        Action(self.taro, "test"))))),
                    "Hana", False),
                ]
        def _checkcode(v, t, expect):
            self.assertEqual(_containsWordIn(v, t), expect)
        validated_testing_withfail(self, "containsWordIn", _checkcode, data)

    def test_containsWordInAction(self):
        data = [
                (False, Action(self.taro, "test"), "test", True),
                (False, Action(self.taro, "test"), "te", True),
                (False, Action(self.taro, "test"), "Taro", True),
                (False, Action(self.taro, "test").d("apple"), "apple", True),
                (False, Action(self.taro, "test").d("orange"), "俺", False),
                (False, CombAction(Action(self.taro, "apple"), Action(self.taro, "orange")),
                    "ple", True),
                (False, TagAction("test"), "test", False),
                ]
        def _checkcode(v, t, expect):
            self.assertEqual(_containsWordInAction(v, t), expect)
        validated_testing_withfail(self, "containsWordInAction", _checkcode, data)

    def test_descriptionCountInAction(self):
        data = [
                (False, Action(self.taro).d("test"), 4,),
                (False, CombAction(Action(self.taro).d("test"), Action(self.taro).d("test")),
                    8,),
                (False, TagAction("", tag_type=TagType.COMMENT), 0,),
                ]
        def _checkcode(v, expect):
            self.assertEqual(_descriptionCountInAction(v), expect)
        validated_testing_withfail(self, "descriptionCountInAction", _checkcode, data)

    def test_descriptionManupaperCountsInAction(self):
        data = [
                (False, Action(self.taro).d("test"), 20, 1,),
                (False, Action(self.taro).d("test"*10), 20, 2,),
                (False, Action(self.taro).d("test"*10), 10, 4,),
                (False, CombAction(Action(self.taro).d("test"), Action(self.taro).d("test"*5)),
                    20, 2,),
                (False, TagAction("", tag_type=TagType.BR),
                    20, 1,),
                ]
        def _checkcode(v, columns, expect):
            self.assertEqual(_descriptionManupaperCountsInAction(v, columns), expect)
        validated_testing_withfail(self, "descriptionManupaperCountsInAction", _checkcode, data)

    def test_dialogueCountInAction(self):
        data = [
                (False, Action(self.taro, act_type=ActType.TALK), self.taro, 1,),
                (False, Action(self.taro), self.taro, 0,),
                (False, Action(self.taro, act_type=ActType.TALK), self.hana, 0,),
                (False, CombAction(Action(self.taro, act_type=ActType.TALK),
                    Action(self.hana, act_type=ActType.TALK)),
                    self.taro, 1,),
                (False, CombAction(Action(self.taro, act_type=ActType.TALK),
                    Action(self.taro, act_type=ActType.TALK)),
                    self.taro, 2,),
                (False, CombAction(Action(self.taro, act_type=ActType.TALK),
                    Action(self.taro, act_type=ActType.TALK)),
                    self.hana, 0,),
                (False, TagAction("", tag_type=TagType.BR), self.taro, 0,),
                ]
        def _checkcode(v, t, expect):
            self.assertEqual(_dialogueCountInAction(v, t), expect)
        validated_testing_withfail(self, "dialogueCountInAction", _checkcode, data)

    def test_dialoguesOfPersonInAction(self):
        data = [
                (False, Action(self.taro, act_type=ActType.TALK).t("test"),
                    self.taro, ["test"],),
                (False, Action(self.taro).t("test"),
                    self.taro, ["test"],),
                (False, Action(self.taro, "test"),
                    self.taro, [],),
                (False, Action(self.taro, act_type=ActType.TALK).t("test"),
                    self.hana, [],),
                (False, CombAction(Action(self.taro, act_type=ActType.TALK).t("test"),
                    Action(self.taro).t("apple"),
                    ), self.taro, ["test", "apple"],),
                (False, TagAction("", tag_type=TagType.COMMENT),
                    self.taro, [],),
                ]
        def _checkcode(v, t, expect):
            tmp = _dialoguesOfPersonInAction(v, t)
            tmp1 = tmp if isinstance(tmp, list) else list(tmp)
            self.assertEqual(tmp1, expect)
        validated_testing_withfail(self, "dialoguesOfPersonInAction", _checkcode, data)

    def test_flagsInAction(self):
        f1 = Flag("test")
        d1 = Flag("apple", True)
        data = [
                (False, Action(self.taro).flag(f1),
                    [f1],),
                (False, Action(self.taro).deflag(d1),
                    [d1],),
                (False, Action(self.taro).flag(f1).deflag(d1),
                    [f1,d1],),
                (False, Action(self.taro), [],),
                (False, CombAction(Action(self.taro).flag(f1), Action(self.taro).deflag(d1),
                    ), [f1, d1],),
                (False, TagAction(""), [],),
                ]
        def _checkcode(v, expect):
            tmp = _flagsInAction(v)
            tmp1 = tmp if isinstance(tmp, list) else list(tmp)
            self.assertEqual(tmp1, expect)
        validated_testing_withfail(self, "flagsInAction", _checkcode, data)

    def test_outlineCountsInAction(self):
        data = [
                (False, Action(self.taro, "test"), 4,),
                (False, CombAction(Action(self.taro, "test"), Action(self.taro, "test"),
                    ), 8,),
                (False, TagAction("test"), 0,),
                ]
        def _checkcode(v, expect):
            self.assertEqual(_outlineCountsInAction(v), expect)
        validated_testing_withfail(self, "outlineCountsInAction", _checkcode, data)

    def test_outlineManupaperCountsInAction(self):
        data = [
                (False, Action(self.taro, "test"), 20, 1,),
                (False, CombAction(Action(self.taro, "test"), Action(self.taro, "test"*5),
                    ), 20, 2,),
                (False, TagAction("test", tag_type=TagType.BR), 20, 1,),
                ]
        def _checkcode(v, columns, expect):
            self.assertEqual(_outlineManupaperCountsInAction(v, columns), expect)
        validated_testing_withfail(self, "outlineManupaperCountsInAction", _checkcode, data)

    def test_personsInAction(self):
        data = [
                (False, Action(self.taro),
                    [self.taro],),
                (False, CombAction(Action(self.taro), Action(self.hana)),
                    [self.taro, self.hana],),
                (False, CombAction(Action(self.taro), Action(self.hana)),
                    [self.taro, self.hana],),
                (False, TagAction("test"),
                    [],),
                ]
        def _checkcode(v, expect):
            self.assertEqual(_personsInAction(v), expect)
        validated_testing_withfail(self, "personsInAction", _checkcode, data)

    def test_math_util_int_ceiled(self):
        data = [
                (False, 10, 3, 4,),
                (False, -10, 3, -3,),
                (True, "1", 1, 1,),
                ]
        def _checkcode(a, b, expect):
            self.assertEqual(int_ceiled(a, b), expect)
        validated_testing_withfail(self, "math_util_int_ceiled", _checkcode, data)
