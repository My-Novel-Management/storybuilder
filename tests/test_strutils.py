# -*- coding: utf-8 -*-
"""Test: strutils.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import strutils as utl


_FILENAME = "strutils.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "strutils methods")

    def test_dict_sorted(self):
        data = [
                (False, {"orange":2, "apple":1}, {"orange":2, "apple":1},),
                (True, {"orange":2, "apple":1}, {"orange":1, "apple":2},),
                (False, {"apples":2, "apple":1}, {"apples":2, "apple":1},),
                ]
        def _checkcode(v, expect):
            self.assertEqual(utl.dict_sorted(v), expect)
            self.assertEqual(
                    [k for k,v in utl.dict_sorted(v).items()],
                    [k for k,v in expect.items()])
        validated_testing_withfail(self, "dict_sorted", _checkcode, data)

    def test_divided_by_splitter(self):
        data = [
                (False, "test,apple", ",", ("test", "apple"),),
                (False, "test,apple", ":", ("test,apple", "test,apple"),),
                (True, "test,apple", 1, ("test", "apple"),),
                (True, 1, ",", 1,),
                ]
        validated_testing_withfail(self, "divided_by_splitter",
                lambda v,sp,expect: self.assertEqual(
                    utl.divided_by_splitter(v, sp), expect), data)

    def test_duplicate_bracket_chop_and_replaced(self):
        data = [
                (False, "「僕は笑う」「君と笑う」", "「僕は笑う。君と笑う」",),
                (False, "「僕は笑う、君と笑う」", "「僕は笑う、君と笑う」",),
                (False, "「僕は笑う。」「君と笑う」", "「僕は笑う。。君と笑う」",),
                (True, 1, 1,),
                ]
        validated_testing_withfail(self, "duplicate_bracket_chop_and_replaced",
                lambda v,expect: self.assertEqual(
                    utl.duplicate_bracket_chop_and_replaceed(v), expect), data)

    def test_extraspace_chopped(self):
        data = [
                (False, "「これはね」　「ですよ」", "「これはね」「ですよ」",),
                (False, "「これはね、　ですよ」", "「これはね、ですよ」",),
                (False, "「これはね。　ですよ」", "「これはね。ですよ」",),
                (True, 1, 1,),
                ]
        validated_testing_withfail(self, "extraspace_chopped",
                lambda v,expect: self.assertEqual(utl.extraspace_chopped(v), expect), data)

    def test_str_duplicated_chopped(self):
        data = [
                (False, "これは。。。", "これは。",),
                (False, "これは、、、", "これは、",),
                (False, "これは、。", "これは、",),
                (False, "これは！。", "これは！　",),
                (False, "これは！、", "これは！　",),
                (False, "これは？。", "これは？　",),
                (False, "これは？、", "これは？　",),
                (False, "これは!?、", "これは!?　",),
                (True, 1, 1,),
                ]
        validated_testing_withfail(self, "str_duplicated_chopped",
                lambda v,expect: self.assertEqual(
                    utl.str_duplicated_chopped(v), expect), data)

    def test_str_replaced_tag_by_dictionary(self):
        data = [
                (False, "$Sは走った", {"S":"太郎"}, "$", "太郎は走った",),
                (False, "$Sは$Sとして走った", {"S":"太郎"}, "$", "太郎は太郎として走った",),
                (False, "$Sは$Hと走った", {"S":"太郎", "H":"花子"}, "$", "太郎は花子と走った",),
                (False, "%Sは走った", {"S":"太郎"}, "%", "太郎は走った",),
                (False, "$Sは$Hと走った", {"S":"太郎"}, "$", "太郎は$Hと走った",),
                (True, 1, {"S":"太郎"}, "$", 1,),
                (True, "$Sは走った", ["S","太郎"], "$", "太郎は走った",),
                (True, "$Sは走った", {"S":"太郎"}, 1, "太郎は走った",),
                ]
        validated_testing_withfail(self, "str_replaced_tag_by_dictionary",
                lambda v,words,pref,expect: self.assertEqual(
                    utl.str_replaced_tag_by_dictionary(v,words,pref),expect), data)

    def test_str_to_dict_by_splitter(self):
        data = [
                (False, {"test":"1"}, {"test":"1"},),
                (False, "test:1", {"test":"1"},),
                (True, 1, 1,),
                ]
        validated_testing_withfail(self, "str_to_dict_by_splitter",
                lambda v,expect: self.assertEqual(
                    utl.str_to_dict_by_splitter(v), expect), data)
