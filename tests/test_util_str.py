# -*- coding: utf-8 -*-
"""Test: util_str.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
import utils.util_str as util


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
                ]
        validatedTestingWithFail(self, "containsWordsIn",
                lambda v, words, expect: self.assertEqual(
                    util.containsWordsIn(v, words), expect), data)

    def test_strDividedBySplitter(self):
        data = [
                (False, "tes,t", ",",
                    ("tes","t")),
                ]
        validatedTestingWithFail(self, "strDividedBySplitter",
                lambda v, sp, expect: self.assertEqual(
                    util.strDividedBySplitter(v, sp), expect), data)

    def test_dictFromStrBySplitter(self):
        data = [
                (False, "ta:Taro:ha:Hana", ":",
                    {"ta":"Taro","ha":"Hana"}),
                (False, {"ta":"Taro"}, "",
                    {"ta":"Taro"}),
                (True, 1, 1,
                    1,),
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
