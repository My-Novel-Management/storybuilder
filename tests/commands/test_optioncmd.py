# -*- coding: utf-8 -*-
'''
OptionParser class test
=======================
'''

import argparse
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands import optioncmd as opt


class OptionParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(opt.__name__, 'OptionParser class')

    def test_instance(self):
        tmp = opt.OptionParser()
        self.assertIsInstance(tmp, opt.OptionParser)

    def test_get_commandline_arguments(self):
        options = ['plot', 'rubi', 'comment', 'debug', 'forcemecab',
                'format', 'priority']
        data = [
                # (is_test, data, expect)
                (True, True, [],
                    [False, False, False, False, False, None, None]),
                (True, True, ['-p'],
                    [True, False, False, False, False, None, None]),
                (True, True, ['--plot'],
                    [True, False, False, False, False, None, None]),
                (True, True, ['-r'],
                    [False, True, False, False, False, None, None]),
                (True, True, ['--rubi'],
                    [False, True, False, False, False, None, None]),
                (True, True, ['--comment'],
                    [False, False, True, False, False, None, None]),
                (True, True, ['--debug'],
                    [False, False, False, True, False, None, None]),
                (True, True, ['--forcemecab'],
                    [False, False, False, False, True, None, None]),
                (True, True, ['--format=w'],
                    [False, False, False, False, False, 'w', None]),
                (True, True, ['--priority=1'],
                    [False, False, False, False, False, None, 1]),
                ]
        def checker(is_test, tdata, expect):
            parser = opt.OptionParser()
            tmp = parser.get_commandline_arguments(is_test, tdata)
            self.assertIsInstance(tmp, argparse.Namespace)
            for arg, exp in zip(options, expect):
                self.assertEqual(getattr(tmp, arg), exp)
        validate_with_fail(self, 'get_commandline_arguments', checker, data)
