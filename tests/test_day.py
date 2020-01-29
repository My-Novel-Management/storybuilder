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

    def test_methods(self):
        data = [
                (False, ("日", 10,5, 2000), "y", 1, ("日・1年後", 2001)),
                (False, ("日", 10,5, 2000), "m", 1, ("日・1月後", 11)),
                (False, ("日", 10,5, 2000), "d", 1, ("日・1日後", 6)),
                ]
        def _checkcode(vals, d, v, expect):
            tmp = Day(*vals)
            if d == "y":
                tmp1 = tmp.elapsedYear(v)
                self.assertEqual(tmp1.name, expect[0])
                self.assertEqual(tmp1.year, expect[1])
            elif d == "m":
                tmp1 = tmp.elapsedMonth(v)
                self.assertEqual(tmp1.name, expect[0])
                self.assertEqual(tmp1.mon, expect[1])
            else:
                tmp1 = tmp.elapsedDay(v)
                self.assertEqual(tmp1.name, expect[0])
                self.assertEqual(tmp1.day, expect[1])
        validatedTestingWithFail(self, "methods", _checkcode, data)

    def test_nextmethods(self):
        tmp = Day("日", 10,5,2000)
        tmp1, tmp2, tmp3 = tmp.nextDay(), tmp.nextMonth(), tmp.nextYear()
        self.assertEqual(tmp1.name, "日・翌日")
        self.assertEqual(tmp2.name, "日・翌月")
        self.assertEqual(tmp3.name, "日・翌年")
        self.assertEqual(tmp1.day, 6)
        self.assertEqual(tmp2.mon, 11)
        self.assertEqual(tmp3.year, 2001)
