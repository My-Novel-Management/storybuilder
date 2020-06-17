# -*- coding: utf-8 -*-
'''
Filter class test
=================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.core import filter as ft


class FilterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(ft.__name__, 'Filter class')

    def test_instance(self):
        tmp = ft.Filter()
        self.assertIsInstance(tmp, ft.Filter)

    def test_execute_internal(self):
        data = [
                # (src, priority, expect, exp_val)
                (True, Chapter('test',
                    Episode('a'), Episode('b'), Episode('c')), 5,
                    True, 3),
                (True, Chapter('test',
                    Episode('a'), Episode('b').set_priority(2), Episode('c')), 5,
                    True, 2),
                (True, Chapter('test',
                    Episode('a'), Episode('b'), Episode('c')), 5,
                    True, 3),
                (True, SCode(None, SCmd.BE, (),'').set_priority(2), 5,
                    True, None),
                ]
        def checker(src, pri, expect, exp_val):
            tmp = ft.Filter()._exec_internal(src, pri)
            self.assertEqual(tmp[1], expect)
            if hasattr(tmp[0], 'children'):
                self.assertEqual(len(tmp[0].children), exp_val)
            elif isinstance(tmp[0], (list, tuple)):
                self.assertEqual(len(tmp[0], exp_val))
            elif tmp[0]:
                self.assertIsInstance(tmp[0], SCode)
            else:
                self.assertEqual(tmp[0], exp_val)
        validate_with_fail(self, 'execute_internal', checker, data)
