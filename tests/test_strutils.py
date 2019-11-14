# -*- coding: utf-8 -*-
"""Test: strutils.py
"""
import unittest
from testutils import print_test_title
from builder import strutils as utl


_FILENAME = "strutils.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "strutils methods")

    def test_dict_sorted(self):
        data = [
                ({"orange":2, "apple":1}, {"apple":1, "orange":2}, False),
                ({"orange":2, "apple":1}, {"orange":2, "apple":1}, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.dict_sorted(v), expect)
                    self.assertEqual(
                            [k for k,v in utl.dict_sorted(v).items()],
                            [k for k,v in expect.items()])
                else:
                    self.assertNotEqual(
                            [k for k,v in utl.dict_sorted(v).items()],
                            [k for k,v in expect.items()])

    def test_divided_by_splitter(self):
        data = [
                ("test,apple", ",", ("test", "apple"), False),
                ("test,apple", ":", ("test,apple", "test,apple"), False),
                ("test,apple", 1, ("test", "apple"), True),
                (1, ",", 1, True),
                ]
        for v, sp, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.divided_by_splitter(v, sp), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(utl.divided_by_splitter(v, sp), expect)

    def test_duplicate_bracket_chop_and_replaced(self):
        data = [
                ("「僕は笑う」「君と笑う」", "「僕は笑う。君と笑う」", False),
                ("「僕は笑う、君と笑う」", "「僕は笑う、君と笑う」", False),
                ("「僕は笑う。」「君と笑う」", "「僕は笑う。。君と笑う」", False),
                (1, 1, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.duplicate_bracket_chop_and_replaceed(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(utl.duplicate_bracket_chop_and_replaceed(v), expect)

    def test_extraspace_chopped(self):
        data = [
                ("「これはね」　「ですよ」", "「これはね」「ですよ」", False),
                ("「これはね、　ですよ」", "「これはね、ですよ」", False),
                ("「これはね。　ですよ」", "「これはね。ですよ」", False),
                (1, 1, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.extraspace_chopped(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(utl.extraspace_chopped(v), expect)

    def test_str_duplicated_chopped(self):
        data = [
                ("これは。。。", "これは。", False),
                ("これは、、、", "これは、", False),
                ("これは、。", "これは、", False),
                ("これは！。", "これは！　", False),
                ("これは！、", "これは！　", False),
                ("これは？。", "これは？　", False),
                ("これは？、", "これは？　", False),
                ("これは!?、", "これは!?　", False),
                (1, 1, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.str_duplicated_chopped(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(utl.str_duplicated_chopped(v), expect)

    def test_str_replaced_tag_by_dictionary(self):
        data = [
                ("$Sは走った", {"S":"太郎"}, "$", "太郎は走った", False),
                ("$Sは$Sとして走った", {"S":"太郎"}, "$", "太郎は太郎として走った", False),
                ("$Sは$Hと走った", {"S":"太郎", "H":"花子"}, "$", "太郎は花子と走った", False),
                ("%Sは走った", {"S":"太郎"}, "%", "太郎は走った", False),
                ("$Sは$Hと走った", {"S":"太郎"}, "$", "太郎は$Hと走った", False),
                (1, {"S":"太郎"}, "$", 1, True),
                ("$Sは走った", ["S","太郎"], "$", "太郎は走った", True),
                ("$Sは走った", {"S":"太郎"}, 1, "太郎は走った", True),
                ]
        for v, words, pref, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.str_replaced_tag_by_dictionary(v, words, pref),
                            expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(utl.str_replaced_tag_by_dictionary(v, words, pref),
                                expect)

    def test_str_to_dict_by_splitter(self):
        data = [
                ({"test":"1"}, {"test":"1"}, False),
                ("test:1", {"test":"1"}, False),
                (1, 1, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(utl.str_to_dict_by_splitter(v), expect)
                else:
                    with self.assertRaises(TypeError):
                        self.assertEqual(utl.str_to_dict_by_splitter(v), expect)
