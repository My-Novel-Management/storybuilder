# -*- coding: utf-8 -*-
'''
ResultData class test
=====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes.builderexception import BuilderError
from builder.datatypes import resultdata as rd


class ResultDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(rd.__name__, 'ResultData class')

    def test_instance(self):
        data = [
                # (data, is_succeeded, error, expect, exp_is_scd, exp_error)
                (True, [1,2,3], True, None,
                    [1,2,3], True, None),
                ]
        def checker(rdata, is_succeeded, error, expect, exp_is_scd, exp_error):
            tmp = rd.ResultData(rdata, is_succeeded, error)
            self.assertIsInstance(tmp, rd.ResultData)
            self.assertEqual(tmp.data, expect)
            self.assertEqual(tmp.is_succeeded, exp_is_scd)
            self.assertEqual(tmp.error, exp_error)
        validate_with_fail(self, 'class instance', checker, data)
