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
        options = ['comment', 'data', 'plot', 'rubi', 'text', 'analyze',
                'console', 'debug',
                'format', 'log', 'part', 'priority',
                ]
        data = [
                # (is_test, data, expect)
                (True, True, [],
                    [False, False, False, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['-c'],
                    [True, False, False, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--comment'],
                    [True, False, False, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['-d'],
                    [False, True, False, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--data'],
                    [False, True, False, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['-p'],
                    [False, False, True, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--plot'],
                    [False, False, True, False, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['-r'],
                    [False, False, False, True, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--rubi'],
                    [False, False, False, True, False, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['-t'],
                    [False, False, False, False, True, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--text'],
                    [False, False, False, False, True, False,
                        False, False,
                        None, None, None, None]),
                (True, True, ['-z'],
                    [False, False, False, False, False, True,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--analyze'],
                    [False, False, False, False, False, True,
                        False, False,
                        None, None, None, None]),
                (True, True, ['--console'],
                    [False, False, False, False, False, False,
                        True, False,
                        None, None, None, None]),
                (True, True, ['--debug'],
                    [False, False, False, False, False, False,
                        False, True,
                        None, None, None, None]),
                (True, True, ['--format=w'],
                    [False, False, False, False, False, False,
                        False, False,
                        'w', None, None, None]),
                (True, True, ['--log=info'],
                    [False, False, False, False, False, False,
                        False, False,
                        None, 'info', None, None]),
                    (True, True, ['--part=0:1'],
                    [False, False, False, False, False, False,
                        False, False,
                        None, None, '0:1', None]),
                (True, True, ['--priority=1'],
                    [False, False, False, False, False, False,
                        False, False,
                        None, None, None, 1]),
                ]
        def checker(is_test, tdata, expect):
            parser = opt.OptionParser()
            tmp = parser.get_commandline_arguments(is_test, tdata)
            self.assertIsInstance(tmp, argparse.Namespace)
            for arg, exp in zip(options, expect):
                self.assertEqual(getattr(tmp, arg), exp)
        validate_with_fail(self, 'get_commandline_arguments', checker, data)
