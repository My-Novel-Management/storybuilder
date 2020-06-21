# -*- coding: utf-8 -*-
'''
Day class test
==============
'''

import datetime
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.objects import day as dy


class DayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(dy.__name__, 'Day class')

    def test_instance(self):
        data = [
                # (name, month, day, year, info, expect, exp_m, exp_d, exp_y, exp_date, exp_info)
                (True, 'test', 1, 10, 1000, 'a note',
                    'test', 1, 10, 1000, datetime.date(1000,1,10), 'a note'),
                (True, '', 1, 10, 1000, 'a note',
                    '', 1, 10, 1000, datetime.date(1000,1,10), 'a note'),
                ]
        def checker(name, mon, day, year, info, expect, exp_m, exp_d, exp_y, exp_date, exp_info):
            tmp = dy.Day(name, mon, day, year, info)
            self.assertIsInstance(tmp, dy.Day)
            self.assertEqual(tmp.name, expect)
            self.assertEqual(tmp.month, exp_m)
            self.assertEqual(tmp.day, exp_d)
            self.assertEqual(tmp.year, exp_y)
            self.assertEqual(tmp.date, exp_date)
            self.assertEqual(tmp.info, exp_info)
        validate_with_fail(self, 'class instance', checker, data)

