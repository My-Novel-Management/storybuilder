# -*- coding: utf-8 -*-
'''
CompileMode Enum class test
===========================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import compilemode as cp


class CompileModeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cp.__name__, 'CompileMode Enum class')

    def test_instance(self):
        self.assertEqual(
                len(cp.CompileMode.get_all()),
                6)

