# -*- coding: utf-8 -*-
"""Test for strutils.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import strutils as utl


_FILENAME = "strutils.py"


class PublicMethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "public methods")

    def test_comma_by(self):
        data = [
                (em.LangType.JPN, "、"),
                (em.LangType.ENG, ", "),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.comma_by(v), expected)

    def test_comment_tag_from(self):
        data = [
                ("test", "<!--test-->"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.comment_tag_from(v), expected)

    def test_description_from(self):
        data = [
                ("test", em.LangType.ENG, 'test.'),
                ("test", em.LangType.JPN, "test。"),
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(utl.description_from(v, lang), expected)

    def test_dialogue_from(self):
        data = [
                ("test", em.LangType.ENG, '"test"'),
                ("test", em.LangType.JPN, "「test」"),
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(utl.dialogue_from(v, lang), expected)

    def test_double_comma_chopped(self):
        data = [
                ("　これを。。ただしく。。", em.LangType.JPN,
                    "　これを。ただしく。"),
                ("　これを、、ただしく、、", em.LangType.JPN,
                    "　これを、ただしく、"),
                (" This is a pen.. the pen. ", em.LangType.ENG,
                    " This is a pen. the pen. "),
                ("これは、。変わらず。、", em.LangType.JPN,
                    "これは、。変わらず。、"),
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(utl.double_comma_chopped(v, lang), expected)

    def test_em_tag_from(self):
        data = [
                ("test", 1, "_test_"),
                ("test", 2, "**test**"),
                ("test", 3, "***test***"),
                ]

        for v, lv, expected in data:
            with self.subTest(v=v, lv=lv, expected=expected):
                self.assertEqual(utl.em_tag_from(v, lv), expected)

    def test_extraend_chopped(self):
        data = [
                ("！。", em.LangType.JPN,
                    "！"),
                ("？。", em.LangType.JPN,
                    "？"),
                ("!. ", em.LangType.ENG,
                    "!"),
                ("?. ", em.LangType.ENG,
                    "?")
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(utl.extraend_chopped(v, lang), expected)

    def test_extraspace_chopped(self):
        data = [
                ("　これを。　ただしくする。", em.LangType.JPN,
                    "　これを。ただしくする。"),
                (" This is a pen.  the pen. ", em.LangType.ENG,
                    " This is a pen. the pen. "),
                ("　これを。、ただしくして。", em.LangType.JPN,
                    "　これを。ただしくして。"),
                ("「これを」　正しくする。", em.LangType.JPN,
                    "「これを」正しくする。"),
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(utl.extraspace_chopped(v, lang), expected)

    def test_head_tag_from(self):
        data = [
                ("test", 1, "# test"),
                ("test", 2, "## test"),
                ]

        for v, lv, expected in data:
            with self.subTest(v=v, lv=lv, expected=expected):
                self.assertEqual(utl.head_tag_from(v, lv), expected)

    def test_hr_tag_from(self):
        data = [
                (1, "--------"),
                (2, "--------"*2),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.hr_tag_from(v), expected)

    def test_is_conversion_attempt(self):
        data = [
                ("test", False),
                ("$test", True),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.is_conversion_attempt(v), expected)

    def test_link_tag_from(self):
        data = [
                ("test", "apple", "[test](apple)"),
                ]

        for v, link, expected in data:
            with self.subTest(v=v, link=link, expected=expected):
                self.assertEqual(utl.link_tag_from(v, link), expected)

    def test_name_divided_from(self):
        data = [
                ("testname", "testname", "testname"),
                ("test,name", "test", "name"),
                ]

        for v, exp_last, exp_name in data:
            with self.subTest(v=v, exp_last=exp_last, exp_name=exp_name):
                self.assertEqual(utl.name_divided_from(v), (exp_last, exp_name))

    def test_paragraph_head_inserted(self):
        data = [
                ("test", em.LangType.ENG, " test"),
                ("test", em.LangType.JPN, "　test"),
                ("「test」", em.LangType.JPN, "「test」"),
                ('"test"', em.LangType.ENG, '"test"'),
                ("# test", em.LangType.ENG, "# test"),
                ("- test", em.LangType.ENG, "- test"),
                (" # test", em.LangType.ENG, " # test"),
                ("    - test", em.LangType.ENG, "    - test"),
                ("　test", em.LangType.JPN, "　test"),
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(utl.paragraph_head_inserted(v, lang), expected)

    def test_quote_tag_from(self):
        data = [
                ("test", "> test"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.quote_tag_from(v), expected)

    def test_reflink_tag_from(self):
        data = [
                ("test", "[test]:test"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.reflink_tag_from(v), expected)

    def test_str_replaced_tag(self):
        data = [
                ("test", {"t":"test"}, "me", "$", "test"),
                ("$kotest", {"ko":"test"}, "me", "$", "testtest"),
                ("$S apple", {"a":"apple"}, "me", "$", "$S apple"),
                ("$S apple", {"me":"test"}, "me", "S", "test apple"),
                ]

        for v, dct, key, pfx, expected in data:
            with self.subTest(v=v, dct=dct, key=key, pfx=pfx, expected=expected):
                self.assertEqual(utl.str_replaced_tag(v, dct, key, pfx), expected)

    def test_str_space_chopped(self):
        data = [
                (" test", "test"),
                (" t e s t", "test"),
                ("　test", "test"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.str_space_chopped(v), expected)

    def test_strike_tag_from(self):
        data = [
                ("test", "~~test~~"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.strike_tag_from(v), expected)

    def test_ul_tag_from(self):
        data = [
                ("test", 1, "    - test"),
                ("test", 2, "        - test"),
                ]

        for v, lv, expected in data:
            with self.subTest(v=v, lv=lv, expected=expected):
                self.assertEqual(utl.ul_tag_from(v, lv), expected)

    def test_ul_tag_space_removed(self):
        data = [
                ("    - test", 1, "- test"),
                ("        - test", 2, "- test"),
                ("        - test", 1, "    - test"),
                ]

        for v, lv, expected in data:
            with self.subTest(v=v, lv=lv, expected=expected):
                self.assertEqual(utl.ul_tag_space_removed(v, lv), expected)

    def test_ul_tag_replaced(self):
        data = [
                ("- test", "*", "* test"),
                ("+ test", "-", "- test"),
                ]

        for v, mark, expected in data:
            with self.subTest(v=v, mark=mark, expected=expected):
                self.assertEqual(utl.ul_tag_replaced(v, mark), expected)
