# -*- coding: utf-8 -*-
'''
SCode class test
================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.command import SCmd
from builder.commands import scode as sc
from builder.objects.sobject import SObject


class SCodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(sc.__name__, 'SCode class')

    def test_instance(self):
        obj = SObject('test')
        data = [
                # (src, cmd, script, option, exp_src, exp_cmd, exp_script, exp_option)
                (True, obj, SCmd.BE, ('apple','orange'), 'a note',
                    obj, SCmd.BE, ('apple','orange'), 'a note'),
                ]
        def checker(src, cmd, script, option, exp_src, exp_cmd, exp_script, exp_option):
            tmp = sc.SCode(src, cmd, script, option)
            self.assertIsInstance(tmp, sc.SCode)
            self.assertEqual(tmp.src, exp_src)
            self.assertEqual(tmp.cmd, exp_cmd)
            self.assertEqual(tmp.script, exp_script)
            self.assertEqual(tmp.option, exp_option)
        validate_with_fail(self, 'class instance', checker, data)

    def test_inherited(self):
        obj0 = SObject('apple')
        obj1 = SObject('orange')
        data = [
                # (src, cmd, script, option, new_src, new_script, new_option,
                #   exp_src, exp_cmd, exp_script, exp_option)
                (True, obj0, SCmd.DO, ('a', 'b'), 'a note',
                    obj1, ('b', 'c'), 'a test',
                    obj1, SCmd.DO, ('b', 'c'), 'a test'),
                ]
        def checker(src, cmd, script, option, new_src, new_script, new_option,
                exp_src, exp_cmd, exp_script, exp_option):
            tmp = sc.SCode(src, cmd, script, option)
            tmp2 = tmp.inherited(new_src, new_script, new_option)
            self.assertIsInstance(tmp2, sc.SCode)
            self.assertEqual(tmp2.src, exp_src)
            self.assertEqual(tmp2.cmd, exp_cmd)
            self.assertEqual(tmp2.script, exp_script)
            self.assertEqual(tmp2.option, exp_option)
        validate_with_fail(self, 'inherited', checker, data)

