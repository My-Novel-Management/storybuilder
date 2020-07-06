# -*- coding: utf-8 -*-
'''
Mathematics utility methods test
================================
'''

import unittest
from testutils import print_testtitle, validate_with_fail
from builder.utils import util_math as umath


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(umath.__name__, 'mathematics-utility methods')

    def test_int_ceil(self):
        data = [
                # (valA, valB, expect)
                (True, 4, 2, 2),
                (True, 5, 2, 3),
                ]
        validate_with_fail(self, "int_ceil",
                lambda v0,v1, expect: self.assertEqual(
                    umath.int_ceil(v0, v1), expect),
                data)

    def test_safe_divided(self):
        data = [
                # (valA, valB, expect)
                (True, 4, 2, 2),
                (True, 5, 0, 0),
                ]
        validate_with_fail(self, 'safe_divided',
                lambda v0, v1, expect: self.assertEqual(
                    umath.safe_divided(v0, v1), expect), data)
