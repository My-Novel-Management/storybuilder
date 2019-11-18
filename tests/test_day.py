# -*- coding: utf-8 -*-
"""Test: day.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import day as dy


_FILENAME = "day.py"


class DayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Day class")

    def test_attributes(self):
        data = [
                (False, "test day", 1, 1, 2000, 1,1,2000,),
                (False, "test day", 1, 1, None, 1,1,dy.Day.__YEAR__,),
                (False, "test day", 1, None, None, 1,dy.Day.__DAY__,dy.Day.__YEAR__,),
                (False, "test day", None, None, None, dy.Day.__MON__,dy.Day.__DAY__,dy.Day.__YEAR__,),
                (True, "test day", 1, 1, "2000", 1,1,2000,),
                (True, "test day", 1, "1", 2000, 1,1,2000,),
                (True, "test day", "1", 1, 2000, 1,1,2000,),
                (True, 1, 1, 1, 2000, 1,1,2000,),
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
        def _checkcode(name, mon1, day1, year1, mon2, day2, year2):
            tmp = _create(name, mon1, day1, year1)
            self.assertIsInstance(tmp, dy.Day)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.mon, mon2)
            self.assertEqual(tmp.day, day2)
            self.assertEqual(tmp.year, year2)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        data = [
                (False, ("apple",1,1,1,), ("apple",11,2,1001),),
                (False, ("apple",1,1,), ("apple",11,2,1000),),
                (False, ("apple",1,), ("apple",11,1,1000),),
                (False, ("apple",), ("apple",10,1,1000),),
                (True, ("apple","1",1,1,), ("apple",11,2,1001),),
                ]
        def _checkcode(vals, expect):
            tmp = dy.Day("test", 10,1,1000)
            tmp1 = tmp.inherited(*vals)
            self.assertIsInstance(tmp1, dy.Day)
            self.assertEqual(tmp1.name, expect[0])
            self.assertEqual(tmp1.mon, expect[1])
            self.assertEqual(tmp1.day, expect[2])
            self.assertEqual(tmp1.year, expect[3])
        validated_testing_withfail(self, "inherited", _checkcode, data)
