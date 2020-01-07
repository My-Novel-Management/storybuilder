# -*- coding: utf-8 -*-
"""Test: util_str.py
"""
## public libs
import datetime
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
import utils.util_str as util
from builder.day import Day


_FILENAME = "util_str.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "util str methods")

    def setUp(self):
        pass

    def test_containsWordsIn(self):
        data = [
                (False, "test", "t", True),
                (False, "apple", ("t","a"), True),
                (False, "test", "a", False),
                (False, "test", ("a","b"), False),
                ]
        validatedTestingWithFail(self, "containsWordsIn",
                lambda v, words, expect: self.assertEqual(
                    util.containsWordsIn(v, words), expect), data)

    def test_daytimeDictSorted(self):
        da1, da2 = Day("a", 1,1,2000), Day("b",1,1,1999)
        data = [
                (False, {"a":da1, "b":da2},
                    {"b":da2,"a":da1}),
                ]
        validatedTestingWithFail(self, "daytimeDictSorted",
                lambda v, expect: self.assertEqual(
                    util.daytimeDictSorted(v), expect), data)

    def test_dictCombined(self):
        data = [
                (False, {"a":"apple"}, {"b":"bar"},
                    {"a":"apple","b":"bar"}),
                ]
        validatedTestingWithFail(self, "dictCombined",
                lambda a, b, expect: self.assertEqual(
                    util.dictCombined(a,b), expect), data)

    def test_dictFromStrBySplitter(self):
        data = [
                (False, "ta:Taro:ha:Hana", ":",
                    {"ta":"Taro","ha":"Hana"}),
                (False, {"ta":"Taro"}, "",
                    {"ta":"Taro"}),
                (True, 1, 1,
                    1,),
                (False, "test", ":", {}),
                ]
        validatedTestingWithFail(self, "dictFromStrBySplitter",
                lambda v, sp, expect: self.assertEqual(
                    util.dictFromStrBySplitter(v, sp), expect), data)

    def test_isAlphabetOnly(self):
        data = [
                (False, "test", True),
                (False, "1test", False),
                (False, "", False),
                (False, None, False),
                ]
        validatedTestingWithFail(self, "isAlphabetOnly",
                lambda v, expect: self.assertEqual(util.isAlphabetsOnly(v), expect), data)

    def test_kanjiOf(self):
        data = [
                (False, "あいうえ尾", ["尾",]),
                (False, "在いうえ尾", ["在", "尾",]),
                ]
        validatedTestingWithFail(self, "kanjiOf",
                lambda v, expect: self.assertEqual(util.kanjiOf(v), expect), data)

    def test_strDividedBySplitter(self):
        data = [
                (False, "tes,t", ",",
                    ("tes","t")),
                ]
        validatedTestingWithFail(self, "strDividedBySplitter",
                lambda v, sp, expect: self.assertEqual(
                    util.strDividedBySplitter(v, sp), expect), data)

    def test_strDuplicatedChopped(self):
        data = [
                (False, "てすと。。", "てすと。"),
                ]
        validatedTestingWithFail(self, "strDuplicatedChopped",
                lambda v, expect: self.assertEqual(
                    util.strDuplicatedChopped(v), expect), data)

    def test_strEllipsis(self):
        data = [
                (False, "あいうえお", 3, "あい…"),
                ]
        validatedTestingWithFail(self, "strEllipsis",
                lambda v,w, expect: self.assertEqual(
                    util.strEllipsis(v,w), expect), data)

    def test_strJoinIf(self):
        data = [
                (False, ["a","pple"], "apple"),
                (False, [], ""),
                (False, None, ""),
                ]
        validatedTestingWithFail(self, "strJoinIf",
                lambda v, expect: self.assertEqual(
                    util.strJoinIf(v), expect), data)

    def test_strReplacedTagByDict(self):
        data = [
                (False, "$taroは食べた", {"taro":"太郎"}, "太郎は食べた"),
                ]
        validatedTestingWithFail(self, "strReplacedTagByDict",
                lambda v, tags, expect: self.assertEqual(
                    util.strReplacedTagByDict(v, tags), expect), data)

    def test_tupleEvenStr(self):
        data = [
                (False, "test", ("test",)),
                (False, ("a",), ("a",)),
                (False, ["1","2"], ("1","2")),
                (True, 1, 1),
                ]
        validatedTestingWithFail(self, "tupleEvenStr",
                lambda v, expect: self.assertEqual(
                    util.tupleEvenStr(v), expect), data)

    def test_tupleFiltered(self):
        data = [
                (False, (1,2,"3"), int, (1,2)),
                ]
        validatedTestingWithFail(self, "tupleFiltered",
                lambda v, t, expect: self.assertEqual(
                    util.tupleFiltered(v, t), expect), data)
