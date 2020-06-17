# -*- coding: utf-8 -*-
'''
FormatMode Enum class test
==========================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import formatmode as fm


class FormatModeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(fm.__name__, 'FormatMode Enum class')

    def test_conv_to_mode(self):
        data = [
                # (mode, expect)
                (True, 'w', fm.FormatMode.WEB),
                (True, 's', fm.FormatMode.SMARTPHONE),
                (True, 'p', fm.FormatMode.PLAIN),
                (True, 'n', fm.FormatMode.DEFAULT),
                ]
        validate_with_fail(self, 'conv_to_mode',
                lambda mode, expect: self.assertEqual(
                    fm.FormatMode.conv_to_mode(mode), expect),
                data)

