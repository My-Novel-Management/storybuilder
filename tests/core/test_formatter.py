# -*- coding: utf-8 -*-
'''
Formatter class test
====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.core import formatter as fm


class FormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(fm.__name__, 'Formatter class')

    def test_instance(self):
        tmp = fm.Formatter()
        self.assertIsInstance(tmp, fm.Formatter)

