# -*- coding: utf-8 -*-
'''
CodeList class test
===================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.datatypes import codelist as cd


class CodeListTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cd.__name__, 'CodeList class')

    def test_instance(self):
        s0 = SCode(None, SCmd.BE, (), '')
        s1 = SCode(None, SCmd.INFO_DATA, (), '')
        data = [
                # (args, expect)
                (True, (s0, s1), (s0, s1)),
                ]
        def checker(args, expect):
            tmp = cd.CodeList(*args)
            self.assertIsInstance(tmp, cd.CodeList)
            self.assertEqual(tmp.data, expect)
        validate_with_fail(self, 'instance', checker, data)

