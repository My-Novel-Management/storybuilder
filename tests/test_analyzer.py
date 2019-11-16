# -*- coding: utf-8 -*-
"""Test: analyzer.py
"""
import unittest
from testutils import print_test_title
from builder.analyzer import Analyzer, int_ceiled
from builder.analyzer import _acttypeCountsInAction
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
from builder.combaction import CombAction
from builder.flag import Flag


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

    def test_acttypeCountsInAction(self):
        data = [
                (Action(self.taro, act_type=ActType.ACT), ActType.ACT, 1, False),
                (Action(self.taro, act_type=ActType.BE), ActType.ACT, 0, False),
                (CombAction(Action(self.taro, act_type=ActType.ACT), Action(self.taro, act_type=ActType.ACT)),
                    ActType.ACT, 2, False),
                (TagAction("", tag_type=TagType.COMMENT), ActType.ACT, 0, False),
                ]
        def _checkcode(v, atype, expect):
            self.assertEqual(_acttypeCountsInAction(v, atype), expect)
        for v, atype, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, atype, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, atype, expect)

    def test_descriptionCountInAction(self):
        data = [
                (Action(self.taro).d("test"), 4, False),
                (CombAction(Action(self.taro).d("test"), Action(self.taro).d("test")),
                    8, False),
                (TagAction("", tag_type=TagType.COMMENT), 0, False),
                ]
        def _checkcode(v, expect):
            self.assertEqual(_descriptionCountInAction(v), expect)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_descriptionManupaperCountsInAction(self):
        data = [
                (Action(self.taro).d("test"), 20, 1, False),
                (Action(self.taro).d("test"*10), 20, 2, False),
                (Action(self.taro).d("test"*10), 10, 4, False),
                (CombAction(Action(self.taro).d("test"), Action(self.taro).d("test"*5)),
                    20, 2, False),
                (TagAction("", tag_type=TagType.BR),
                    20, 1, False),
                ]
        def _checkcode(v, columns, expect):
            self.assertEqual(_descriptionManupaperCountsInAction(v, columns), expect)
        for v, columns, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, columns, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, columns, expect)

    def test_dialogueCountInAction(self):
        data = [
                (Action(self.taro, act_type=ActType.TALK), self.taro, 1, False),
                (Action(self.taro), self.taro, 0, False),
                (Action(self.taro, act_type=ActType.TALK), self.hana, 0, False),
                (CombAction(Action(self.taro, act_type=ActType.TALK),
                    Action(self.hana, act_type=ActType.TALK)),
                    self.taro, 1, False),
                (CombAction(Action(self.taro, act_type=ActType.TALK),
                    Action(self.taro, act_type=ActType.TALK)),
                    self.taro, 2, False),
                (CombAction(Action(self.taro, act_type=ActType.TALK),
                    Action(self.taro, act_type=ActType.TALK)),
                    self.hana, 0, False),
                (TagAction("", tag_type=TagType.BR), self.taro, 0, False),
                ]
        def _checkcode(v, t, expect):
            self.assertEqual(_dialogueCountInAction(v, t), expect)
        for v, t, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, t, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, t, expect)

    def test_dialoguesOfPersonInAction(self):
        data = [
                (Action(self.taro, act_type=ActType.TALK).t("test"),
                    self.taro, ["test"], False),
                (Action(self.taro).t("test"),
                    self.taro, ["test"], False),
                (Action(self.taro, "test"),
                    self.taro, [], False),
                (Action(self.taro, act_type=ActType.TALK).t("test"),
                    self.hana, [], False),
                (CombAction(Action(self.taro, act_type=ActType.TALK).t("test"),
                    Action(self.taro).t("apple"),
                    ), self.taro, ["test", "apple"], False),
                (TagAction("", tag_type=TagType.COMMENT),
                    self.taro, [], False),
                ]
        def _checkcode(v, t, expect):
            tmp = _dialoguesOfPersonInAction(v, t)
            tmp1 = tmp if isinstance(tmp, list) else list(tmp)
            self.assertEqual(tmp1, expect)
        for v, t, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, t, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, t, expect)

    def test_flagsInAction(self):
        f1 = Flag("test")
        d1 = Flag("apple", True)
        data = [
                (Action(self.taro).flag(f1),
                    [f1], False),
                (Action(self.taro).deflag(d1),
                    [d1], False),
                (Action(self.taro).flag(f1).deflag(d1),
                    [f1,d1], False),
                (Action(self.taro), [], False),
                (CombAction(Action(self.taro).flag(f1), Action(self.taro).deflag(d1),
                    ), [f1, d1], False),
                (TagAction(""), [], False),
                ]
        def _checkcode(v, expect):
            tmp = _flagsInAction(v)
            tmp1 = tmp if isinstance(tmp, list) else list(tmp)
            self.assertEqual(tmp1, expect)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_outlineCountsInAction(self):
        data = [
                (Action(self.taro, "test"), 4, False),
                (CombAction(Action(self.taro, "test"), Action(self.taro, "test"),
                    ), 8, False),
                (TagAction("test"), 0, False),
                ]
        def _checkcode(v, expect):
            self.assertEqual(_outlineCountsInAction(v), expect)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_outlineManupaperCountsInAction(self):
        data = [
                (Action(self.taro, "test"), 20, 1, False),
                (CombAction(Action(self.taro, "test"), Action(self.taro, "test"*5),
                    ), 20, 2, False),
                (TagAction("test", tag_type=TagType.BR), 20, 1, False),
                ]
        def _checkcode(v, columns, expect):
            self.assertEqual(_outlineManupaperCountsInAction(v, columns), expect)
        for v, columns, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, columns, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, columns, expect)

    def test_personsInAction(self):
        data = [
                (Action(self.taro),
                    [self.taro], False),
                (CombAction(Action(self.taro), Action(self.hana)),
                    [self.taro, self.hana], False),
                (CombAction(Action(self.taro), Action(self.hana)),
                    [self.taro, self.hana], False),
                (TagAction("test"),
                    [], False),
                ]
        def _checkcode(v, expect):
            self.assertEqual(_personsInAction(v), expect)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_math_util_int_ceiled(self):
        data = [
                (10, 3, 4, False),
                (-10, 3, -3, False),
                ("1", 1, 1, True),
                ]
        def _checkcode(a, b, expect):
            self.assertEqual(int_ceiled(a, b), expect)
        for a, b, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(a, b, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(a, b, expect)
