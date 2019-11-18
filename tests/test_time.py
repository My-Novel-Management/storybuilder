# -*- coding: utf-8 -*-
"""Test: time.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.time import Time


_FILENAME = "time.py"


class TimeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Time class")

    def test_attributes(self):
        data = [
                (False, "test", 10, 5, 1,
                    10, 5, 1,),
                (False, "test", 10, 5, None,
                    10, 5, Time.__SEC__,),
                (False, "test", 10, None, None,
                    10, Time.__MIN__, Time.__SEC__,),
                (False, "tets", None, None, None,
                    Time.__HOUR__, Time.__MIN__, Time.__SEC__,),
                (True, 1, 1,1,1,
                    1,1,1,),
                ]
        def _create(name, hour, min, sec):
            if sec:
                return Time(name, hour, min, sec)
            elif min:
                return Time(name, hour, min)
            elif hour:
                return Time(name, hour)
            else:
                return Time(name)
        def _checkcode(name, hour1, min1, sec1, hour2, min2, sec2):
            tmp = _create(name, hour1, min1, sec1)
            self.assertIsInstance(tmp, Time)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.hour, hour2)
            self.assertEqual(tmp.min, min2)
            self.assertEqual(tmp.sec, sec2)
            self.assertEqual(tmp.numsys, Time.__DEF_NUMSYS__)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_setNumsys(self):
        base_hour, base_min, base_sec = 10, 5, 1
        data = [
                (False, 10, 10,),
                (True, -1, -1,),
                (True, 1000, 1000,),
                ]
        def _checkcode(v, expect):
            tmp = Time("test", base_hour, base_min, base_sec)
            self.assertEqual(tmp.numsys, Time.__DEF_NUMSYS__)
            tmp.setNumsys(v)
            self.assertEqual(tmp.numsys, expect)
        validated_testing_withfail(self, "setNumsys", _checkcode, data)

    def test_inherited(self):
        base_name, base_hour, base_min, base_sec = "test", 10, 5, 1
        data = [
                (False, "apple", 1, 1, 1,
                    "apple", base_hour+1, base_min+1, base_sec+1,),
                (False, "orange", 1, 1, None,
                    "orange", base_hour+1, base_min+1, base_sec,),
                (False, "pain", 1, None, None,
                    "pain", base_hour+1, base_min, base_sec,),
                (False, "banana", None, None, None,
                    "banana", base_hour, base_min, base_sec,),
                (True, 1, 1,1,1,
                    1,1,1,1,),
                ]
        def _create(time: Time, name, hour, min, sec):
            if sec:
                return time.inherited(name, hour, min, sec)
            elif min:
                return time.inherited(name, hour, min)
            elif hour:
                return time.inherited(name, hour)
            else:
                return time.inherited(name)
        def _checkcode(name1, hour1, min1, sec1, name2, hour2, min2, sec2):
            tmp = Time(base_name, base_hour, base_min, base_sec)
            tmp1 = _create(tmp, name1, hour1, min1, sec1)
            self.assertIsInstance(tmp1, Time)
            self.assertEqual(tmp1.name, name2)
            self.assertEqual(tmp1.hour, hour2)
            self.assertEqual(tmp1.min, min2)
            self.assertEqual(tmp1.sec, sec2)
        validated_testing_withfail(self, "inherited", _checkcode, data)
