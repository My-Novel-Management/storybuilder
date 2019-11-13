# -*- coding: utf-8 -*-
"""Test for day.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import day as dy


_FILENAME = "day.py"


class DayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Day class")

    def test_attributes(self):
        data = [
                ("test1", 1, 10, 2000, 12, 30, "a note",
                    "test1", 1, 10, 2000, 12, 30, "a note"),
                ("test2", 2, 11, 2001, 13, 31, "",
                    "test2", 2, 11, 2001, 13, 31, ""),
                ("test3", 3, 12, 2002, 14, 32, "",
                    "test3", 3, 12, 2002, 14, 32, ""),
                ("test4", 4, 13, 2003, 15, None, "",
                    "test4", 4, 13, 2003, 15, 0, ""),
                ("test5", 5, 14, 2004, None, None, "",
                    "test5", 5, 14, 2004, 0, 0, ""),
                ("test6", 6, 15, None, None, None, "",
                    "test6", 6, 15, 0, 0, 0, ""),
                ("test7", 7, None, None, None, None, "",
                    "test7", 7, 0, 0, 0, 0, ""),
                ("test8", None, None, None, None, None, "",
                    "test8", 0, 0, 0, 0, 0, ""),
                ]

        def creator(name, mon, day, year, hour, mi, note):
            if mon and day and year and hour and mi and note:
                return dy.Day(name, mon, day, year, hour, mi, note)
            elif mon and day and year and hour and mi:
                return dy.Day(name, mon, day, year, hour, mi)
            elif mon and day and year and hour:
                return dy.Day(name, mon, day, year, hour)
            elif mon and day and year:
                return dy.Day(name, mon, day, year)
            elif mon and day:
                return dy.Day(name, mon, day)
            elif mon:
                return dy.Day(name, mon)
            else:
                return dy.Day(name)

        for name, mon, day, year, hour, mi, note, exp_name, exp_mon, exp_day, exp_year, exp_hour, exp_mi, exp_note in data:
            with self.subTest(name=name, mon=mon, day=day, year=year, hour=hour, mi=mi, note=note,
                exp_name=exp_name, exp_mon=exp_mon, exp_day=exp_day, exp_hour=exp_hour,
                exp_mi=exp_mi, exp_note=exp_note):
                tmp = creator(name, mon, day, year, hour, mi, note)
                self.assertIsInstance(tmp,dy.Day)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.mon, exp_mon)
                self.assertEqual(tmp.day, exp_day)
                self.assertEqual(tmp.year, exp_year)
                self.assertEqual(tmp.hour, exp_hour)
                self.assertEqual(tmp.min, exp_mi)
                self.assertEqual(tmp.note, exp_note)

