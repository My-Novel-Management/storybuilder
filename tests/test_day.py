# -*- coding: utf-8 -*-
"""Test: day.py
"""
import unittest
from testutils import print_test_title
from builder import day as dy


_FILENAME = "day.py"


class DayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Day class")

    def test_attributes(self):
        data = [
                ("test day", 1, 1, 2000, 1,1,2000, False),
                ("test day", 1, 1, None, 1,1,dy.Day.__YEAR__, False),
                ("test day", 1, None, None, 1,dy.Day.__DAY__,dy.Day.__YEAR__, False),
                ("test day", None, None, None, dy.Day.__MON__,dy.Day.__DAY__,dy.Day.__YEAR__, False),
                ("test day", 1, 1, "2000", 1,1,2000, True),
                ("test day", 1, "1", 2000, 1,1,2000, True),
                ("test day", "1", 1, 2000, 1,1,2000, True),
                (1, 1, 1, 2000, 1,1,2000, True),
                ]
        def _create(name, mon, day, year):
            if year:
                return dy.Day(name, mon, day, year)
            elif day:
                return dy.Day(name, mon, day)
            elif mon:
                return dy.Day(name, mon)
            else:
                return dy.Day(name)
        for name, mon, day, year, exp_mon, exp_day, exp_year, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = _create(name, mon, day, year)
                    self.assertIsInstance(tmp, dy.Day)
                    self.assertEqual(tmp.name, name)
                    self.assertEqual(tmp.mon, exp_mon)
                    self.assertEqual(tmp.day, exp_day)
                    self.assertEqual(tmp.year, exp_year)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = _create(name, mon, day, year)
                        self.assertIsInstance(tmp, dy.Day)
                        self.assertEqual(tmp.name, name)
                        self.assertEqual(tmp.mon, exp_mon)
                        self.assertEqual(tmp.day, exp_day)
                        self.assertEqual(tmp.year, exp_year)

    def test_inherited(self):
        data = [
                (("apple",1,1,1,), ("apple",11,2,1001), False),
                (("apple",1,1,), ("apple",11,2,1000), False),
                (("apple",1,), ("apple",11,1,1000), False),
                (("apple",), ("apple",10,1,1000), False),
                (("apple","1",1,1,), ("apple",11,2,1001), True),
                ]
        for vals, expect, isfail in data:
            with self.subTest():
                tmp = dy.Day("test", 10,1,1000)
                if not isfail:
                    tmp1 = tmp.inherited(*vals)
                    self.assertIsInstance(tmp1, dy.Day)
                    self.assertEqual(tmp1.name, expect[0])
                    self.assertEqual(tmp1.mon, expect[1])
                    self.assertEqual(tmp1.day, expect[2])
                    self.assertEqual(tmp1.year, expect[3])
                else:
                    with self.assertRaises(AssertionError):
                        tmp1 = tmp.inherited(*vals)
                        self.assertIsInstance(tmp1, dy.Day)
                        self.assertEqual(tmp1.name, expect[0])
                        self.assertEqual(tmp1.mon, expect[1])
                        self.assertEqual(tmp1.day, expect[2])
                        self.assertEqual(tmp1.year, expect[3])
