# -*- coding: utf-8 -*-
"""Test: day.py
"""
## public libs
import unittest
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
        attrs = ("mon", "day", "year", "note",)
        data = [
                (False, "test", 2,3, 1990, "a day",
                    (2,3, 1990, "a day")),
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
        def _checkcode(name, mon, day, year, note, expects):
            tmp = _creator(name, mon, day, year, note)
            self.assertIsInstance(tmp, Day)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

