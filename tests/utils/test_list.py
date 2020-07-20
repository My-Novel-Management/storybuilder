# -*- coding: utf-8 -*-
'''
List utility methods test
=========================
'''

import unittest
from testutils import print_testtitle, validate_with_fail
from builder.utils import util_list as utl


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(utl.__name__, 'list-utility methods')

    def test_list_without_none(self):
        data = [
                # (val, expect)
                (True, [1,2,3, None, 5], [1,2,3,5]),
                ]
        validate_with_fail(self, 'list_without_none',
                lambda val, expect: self.assertEqual(
                    utl.list_without_none(val), expect),
                data)

