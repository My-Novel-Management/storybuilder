# -*- coding: utf-8 -*-
'''
Compiler class test
===================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.datatypes.codelist import CodeList
from builder.datatypes.formattag import FormatTag
from builder.datatypes.rawdata import RawData
from builder.objects.rubi import Rubi
from builder.core import compiler as cp


class CompilerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cp.__name__, 'Compiler class')

    def test_instance(self):
        tmp = cp.Compiler()
        self.assertIsInstance(tmp, cp.Compiler)

    def test_conv_to_novel(self):
        data = [
                # (src, is_cmt, expect)
                (True, CodeList(*[SCode(None, SCmd.BE, ('太郎',),'')]),
                    False,
                    (FormatTag.DESCRIPTION_HEAD, '　太郎。','\n')),
                ]
        validate_with_fail(self, 'conv_to_novel',
                lambda src, is_cmt, expect: self.assertEqual(
                    cp.Compiler()._conv_to_novel(src, is_cmt).data, expect),
                data)

    def test_add_rubi_on_novel(self):
        data = [
                # (src, rubis, expect)
                (True, RawData(*['暫くすると',]),
                    {'暫く': Rubi('暫く', '暫《しばら》く')},
                    ('暫《しばら》くすると',)),
                ]
        validate_with_fail(self, 'add_rubi_on_novel',
                lambda src, rubis, expect: self.assertEqual(
                    cp.Compiler()._add_rubi_on_novel(src, rubis).data, expect),
                data)

    def test_conv_from_tag(self):
        data = [
                # (src, head, nums, is_cmt, is_plot, is_data, in_mate, expect, exp_nums)
                (True, SCode(None, SCmd.TAG_BR, (), ''), '#', (1,1,1),
                    True, False, False, False,
                    '\n\n', (1,1,1)),
                ]
        def checker(src, head, nums, is_cmt, is_plot, is_data, in_mate, expect, exp_nums):
            tmp = cp.Compiler()._conv_from_tag(src, head, nums, is_cmt, is_plot, is_data, in_mate)
            self.assertEqual(tmp[0], expect)
            self.assertEqual(tmp[1], exp_nums)
        validate_with_fail(self, 'conv_from_tag', checker, data)
