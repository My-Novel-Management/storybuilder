# -*- coding: utf-8 -*-
'''
Dictionary utility methods test
===============================
'''

import unittest
from testutils import print_testtitle, validate_with_fail
from builder.utils import util_dict as udict


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(udict.__name__, 'dictionary-utility methods')

    def test_calling_dict_from(self):
        data = [
                # (calling, name, expect)
                (True, "A:test", "taro", {"A":"test","S":"taro","M":"私"}),
                ]
        validate_with_fail(self, 'calling_dict_from',
                lambda calling,name,expect: self.assertEqual(
                    udict.calling_dict_from(calling, name), expect),
                data)

    def test_combine_dict(self):
        data = [
                # (dictA, dictB, expect)
                (True, {'a':'apple'}, {'b':'ball'}, {'a':'apple', 'b':'ball'}),
                ]
        validate_with_fail(self, "combine_dict",
                lambda v0,v1, expect: self.assertEqual(
                    udict.combine_dict(v0, v1), expect),
                data)

    def test_dict_sorted(self):
        data = [
                # (dict, is_reverse, expect)
                (True, {'b':'ball', 'a':'apple', 'c':'can'}, False,
                    {'a':'apple', 'b':'ball', 'c':'can'}),
                ]
        validate_with_fail(self, 'dict_sorted',
                lambda v,is_rev, expect: self.assertEqual(
                    udict.dict_sorted(v, is_rev), expect),
                data)
