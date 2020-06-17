# -*- coding: utf-8 -*-
'''
FormatTag Enum class test
==========================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import formattag as fm


class FormatTagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(fm.__name__, 'FormatTag Enum class')

    def test_instance(self):
        self.assertEqual(
                len(fm.FormatTag.get_all()),
                4)

