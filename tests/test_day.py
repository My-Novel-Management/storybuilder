# -*- coding: utf-8 -*-
"""Test: day.py
"""
## public libs
import unittest
import datetime
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.day import Day


_FILENAME = "day.py"


class DayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Day class")

    def setUp(self):
        pass

    def test_attributes(self):
        data = [
                (False, "test", 2,3, 1990, "a day",
                    datetime.date(1990, 2,3), "a day"),
                ]
        def _creator(name, mon, day, year, note):
            if mon and day and year and note:
                return Day(name, mon, day, year, note)
            elif mon and day and year:
                return Day(name, mon, day, year)
            elif mon and day:
                return Day(name, mon, day)
            elif mon:
                return Day(name, mon)
            else:
                return Day(name)
        def _checkcode(name, mon, day, year, note, expect, exp_note):
            tmp = _creator(name, mon, day, year, note)
            self.assertIsInstance(tmp, Day)
            self.assertEqual(tmp.data, expect)
            self.assertEqual(tmp.note, exp_note)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

