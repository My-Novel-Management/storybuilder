# -*- coding: utf-8 -*-
'''
Writer class test
=================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.objects.sobject import SObject
from builder.world import Writer


class WriterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle("world.Writer", 'Writer class')

    def test_instance(self):
        taro = SObject('taro')
        data = [
                # (src, act, args, exp_src, exp_cmd, exp_args)
                (True, taro, 'be', ('a',),
                    taro, SCmd.BE, ('a',)),
                (True, taro, 'come', ('a',),
                    taro, SCmd.COME, ('a',)),
                (True, taro, 'do', ('a',),
                    taro, SCmd.DO, ('a',)),
                (True, taro, 'explain', ('a',),
                    taro, SCmd.EXPLAIN, ('a',)),
                (True, taro, 'go', ('a',),
                    taro, SCmd.GO, ('a',)),
                (True, taro, 'hear', ('a',),
                    taro, SCmd.HEAR, ('a',)),
                (True, taro, 'look', ('a',),
                    taro, SCmd.LOOK, ('a',)),
                (True, taro, 'talk', ('a',),
                    taro, SCmd.TALK, ('a',)),
                (True, taro, 'think', ('a',),
                    taro, SCmd.THINK, ('a',)),
                (True, taro, 'voice', ('a',),
                    taro, SCmd.VOICE, ('a',)),
                (True, taro, 'wear', ('a',),
                    taro, SCmd.WEAR, ('a',)),
                ]
        def checker(src, act, args, exp_src, exp_cmd, exp_args):
            tmp = Writer(src)
            self.assertIsInstance(tmp, Writer)
            tmp2 = getattr(tmp, act)(*args)
            self.assertIsInstance(tmp2, SCode)
            self.assertEqual(tmp2.src, exp_src)
            self.assertEqual(tmp2.cmd, exp_cmd)
            self.assertEqual(tmp2.script, exp_args)
        validate_with_fail(self, 'class instance', checker, data)

