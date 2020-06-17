# -*- coding: utf-8 -*-
'''
Time class test
===============
'''

import datetime
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.objects import time as tm


class TimeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(tm.__name__, 'Time class')

    def test_instance(self):
        data = [
                # (name, hour, minute, expect, exp_h, exp_m, exp_time)
                (True, 'test', 5, 20, 'test', 5, 20, datetime.time(5,20)),
                ]
        def checker(name, hour, minute, expect, exp_h, exp_m, exp_time):
            tmp = tm.Time(name, hour, minute)
            self.assertIsInstance(tmp, tm.Time)
            self.assertEqual(tmp.name, expect)
            self.assertEqual(tmp.hour, exp_h)
            self.assertEqual(tmp.minute, exp_m)
            self.assertEqual(tmp.time, exp_time)
        validate_with_fail(self, 'class instance', checker, data)

