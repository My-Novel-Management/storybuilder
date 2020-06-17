# -*- coding: utf-8 -*-
'''
Converter class test
====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.tools import converter as cnv


class ConverterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cnv.__name__, 'Converter class')

    def test_add_rubi(self):
        data = [
                # (src, key, rubi, num, expect)
                (True, '山田太郎', '太郎', '太郎《たろう》', 1, '山田太郎《たろう》'),
                ]
        validate_with_fail(self, 'add_rubi',
                lambda src, key, rubi, num, expect: self.assertEqual(
                    cnv.Converter().add_rubi(src, key, rubi, num), expect),
                data)

    def test_to_description(self):
        data = [
                # (src, expect)
                (True, ['太郎は、', '天才だ'], '太郎は、天才だ。'),
                ]
        validate_with_fail(self, 'to_description',
                lambda src, expect: self.assertEqual(
                    cnv.Converter().to_description(src), expect),
                data)

    def test_to_dialogue(self):
        data = [
                # (src, expect)
                (True, ['お前は、', 'どういうつもりだ？'],
                    '「お前は、どういうつもりだ？」'),
                ]
        validate_with_fail(self, 'to_dialogue',
                lambda src, expect: self.assertEqual(
                    cnv.Converter().to_dialogue(src), expect),
                data)

    def test_script_relieved_symbols(self):
        data = [
                # (src, expect)
                (True, ['a', '&'], ['a',]),
                ]
        validate_with_fail(self, 'script_relieved_symbols',
                lambda src, expect: self.assertEqual(
                    cnv.Converter().script_relieved_symbols(src), expect),
                data)
