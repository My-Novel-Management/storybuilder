# -*- coding: utf-8 -*-
'''
String utility methods test
===========================
'''

import unittest
from testutils import print_testtitle, validate_with_fail
from builder.utils import util_str as ustr


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(ustr.__name__, 'string-utility methods')

    def test_dict_from_string(self):
        data = [
                # (val, splitter, expect)
                (True, "a:test", ":", {"a":"test"}),
                ]
        validate_with_fail(self, "dict_from_string",
                lambda v,splt, expect: self.assertEqual(
                    ustr.dict_from_string(v,splt), expect),
                data)


    def test_hiragana_list_from(self):
        data = [
                # (val, expect)
                (True, 'あい１２３', ['あ', 'い']),
                ]
        validate_with_fail(self, 'hiragana_list_from',
                lambda v, expect: self.assertEqual(
                    ustr.hiragana_list_from(v), expect), data)


    def test_kanji_list_from(self):
        data = [
                # (val, expect)
                (True, 'あいう漢お', ['漢',]),
                ]
        validate_with_fail(self, 'kanji_list_from',
                lambda v, expect: self.assertEqual(
                    ustr.kanji_list_from(v), expect), data)


    def test_katakana_list_from(self):
        data = [
                # (val, expect)
                (True, 'あいうエお', ['エ']),
                ]
        validate_with_fail(self, 'katakana_list_from',
                lambda v, expect: self.assertEqual(
                    ustr.katakana_list_from(v), expect), data)


    def test_string_replaced_by_tag(self):
        data = [
                # (val, tags, prefix, expect)
                (True, '$test apple', {'test':'AN'}, '$', 'AN apple'),
                ]
        validate_with_fail(self, 'string_replaced_by_tag',
                lambda v,tags,prefix, expect: self.assertEqual(
                    ustr.string_replaced_by_tag(v, tags, prefix), expect),
                data)

    def test_validate_string_duplicate_chopped(self):
        data = [
                # (val, expect)
                (True, '太郎。。', '太郎。'),
                (True, '太郎、、', '太郎、'),
                (True, '太郎。、', '太郎。'),
                (True, '太郎、。', '太郎、'),
                (True, '？、', '？　'),
                (True, '！。', '！　'),
                (True, '？。', '？　'),
                ]
        validate_with_fail(self, 'validate_string_duplicate_chopped',
                lambda v, expect: self.assertEqual(
                    ustr.validate_string_duplicate_chopped(v), expect),
                data)
