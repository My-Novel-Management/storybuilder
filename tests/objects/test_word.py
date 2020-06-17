# -*- coding: utf-8 -*-
'''
Word class test
===============
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.objects import word as wd


class WordTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(wd.__name__, 'Word class')

    def test_instance(self):
        data = [
                # (name, cate, info, expect, exp_cate, exp_info)
                (True, 'test', 'T', 'a note', 'test', 'T', 'a note'),
                ]
        def checker(name, cate, info, expect, exp_cate, exp_info):
            tmp = wd.Word(name, cate, info)
            self.assertIsInstance(tmp, wd.Word)
            self.assertEqual(tmp.name, expect)
            self.assertEqual(tmp.category, exp_cate)
            self.assertEqual(tmp.info, exp_info)
        validate_with_fail(self, 'class instance', checker, data)

