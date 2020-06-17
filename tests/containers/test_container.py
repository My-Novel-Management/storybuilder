# -*- coding: utf-8 -*-
'''
Container class test
====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.containers import container as cnt


class ContainerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cnt.__name__, 'Container class')

    def test_instance(self):
        data = [
                # (title, args, outline, exp_title, exp_args, exp_outline)
                (True, 'test', ('apple','orange'), 'a note',
                    'test', ('apple','orange'), 'a note'),
                ]
        def checker(title, args, outline, exp_title, exp_args, exp_outline):
            tmp = cnt.Container(title, *args, outline=outline)
            self.assertIsInstance(tmp, cnt.Container)
            self.assertEqual(tmp.title, exp_title)
            self.assertEqual(tmp.children, exp_args)
            self.assertEqual(tmp.outline, exp_outline)
        validate_with_fail(self, 'class instance', checker, data)

    def test_inherited(self):
        data = [
                # (title, args, outline, new_title, new_args, new_outline,
                #   exp_title, exp_args, exp_outline)
                (True, 'test', ('a','b',), 'apple',
                    'test2', ('b','c',), 'orange',
                    'test2', ('b','c'), 'orange'),
                ]
        def checker(title, args, outline, new_title, new_args, new_outline, exp_title, exp_args, exp_outline):
            tmp = cnt.Container(title, *args, outline=outline)
            self.assertEqual(tmp.title, title)
            self.assertEqual(tmp.children, args)
            self.assertEqual(tmp.outline, outline)
            tmp2 = tmp.inherited(*new_args, title=new_title, outline=new_outline)
            self.assertIsInstance(tmp2, cnt.Container)
            self.assertEqual(tmp2.title, exp_title)
            self.assertEqual(tmp2.children, exp_args)
            self.assertEqual(tmp2.outline, exp_outline)
        validate_with_fail(self, 'inherited', checker, data)

