# -*- coding: utf-8 -*-
'''
Checker class test
==================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.tools import checker as ck


class CheckerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(ck.__name__, 'Item class')

    def test_has_rubi_exclusions(self):
        data = [
                # (src, exwords, expect)
                (True, '太郎', ['太郎',], True),
                ]
        validate_with_fail(self, 'has_rubi_exclusions',
                lambda src, exwords, expect: self.assertEqual(
                    ck.Checker().has_rubi_exclusions(src, exwords), expect),
                data)

    def test_has_rubi_key(self):
        data = [
                # (src, key, expect[bool])
                (True, 'test', 't', True),
                ]
        validate_with_fail(self, 'has_rubi_key',
                lambda src,key,expect: self.assertEqual(
                    ck.Checker().has_rubi_key(src, key), expect),
                data)

    def test_has_rubi_key_converted(self):
        data = [
                # (src, key, expect[bool])
                (True, '｜太郎', '太郎', True),
                ]
        validate_with_fail(self, 'has_rubi_key_converted',
                lambda src,key,expect: self.assertEqual(
                    ck.Checker().has_rubi_key_converted(src, key), expect),
                data)

    def test_has_tag_comment(self):
        data = [
                # (src, expect[bool])
                (True, '<!--comment-->', True),
                ]
        validate_with_fail(self, 'has_tag_comment',
                lambda src, expect: self.assertEqual(
                    ck.Checker().has_tag_comment(src), expect),
                data)

    def test_has_tag_symbol(self):
        data = [
                # (src, symbol, expect)
                (True, '$taroはね', '$', True),
                (True, '俺は$taroだ', '$', True),
                ]
        validate_with_fail(self, 'has_tag_symbol',
                lambda src, symbol, expect: self.assertEqual(
                    ck.Checker().has_tag_symbol(src, symbol), expect),
                data)

    def test_has_tag_top(self):
        data = [
                # (src, expect[bool])
                (True, '# head', True),
                ]
        validate_with_fail(self, 'has_tag_top',
                lambda src, expect: self.assertEqual(
                    ck.Checker().has_tag_top(src), expect),
                data)

    def test_has_then(self):
        data = [
                # (src, expect[bool])
                (True, SCode(None, SCmd.THEN, (),""), True),
                ]
        validate_with_fail(self, 'has_then',
                lambda src, expect: self.assertEqual(
                    ck.Checker().has_then(src), expect),
                data)

    def test_is_breakline(self):
        data = [
                # (src, expect[bool])
                (True, '\n', True),
                ]
        validate_with_fail(self, 'is_breakline',
                lambda src, expect: self.assertEqual(
                    ck.Checker().is_breakline(src), expect),
                data)

    def test_is_empty_script(self):
        data = [
                # (src, expect[bool])
                (True, SCode(None, SCmd.BE, ('&',), ""), True),
                ]
        validate_with_fail(self, 'is_empty_script',
                lambda src, expect: self.assertEqual(
                    ck.Checker().is_empty_script(src), expect),
                data)
