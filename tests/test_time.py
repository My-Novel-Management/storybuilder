# -*- coding: utf-8 -*-
"""Test: time.py
"""
## public libs
import datetime
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.time import Time


_FILENAME = "time.py"


class TimeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Time class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("hour", "min", "sec", "note",)
        data = [
                (False, "test", 12, 1, 5, "a time",
                    datetime.time(12, 1, 5), "a time"),
                ]
        def _checkcode(name, hour, min, sec, note, expect, exp_note):
            tmp = Time(name, hour, min, sec, note=note)
            self.assertIsInstance(tmp, Time)
            self.assertEqual(tmp.data, expect)
            self.assertEqual(tmp.note, exp_note)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_attributes2(self):
        data = [
                (False, 12, 1, 5),
                ]
        def _checkcode(h, m, s):
            tmp = Time("test", h, m, s)
            self.assertEqual(tmp.hour, h)
            self.assertEqual(tmp.minute, m)
            self.assertEqual(tmp.second, s)
        validatedTestingWithFail(self, "class hour,minute,second", _checkcode, data)

    def test_methods(self):
        data = [
                (False, ("日", 12,5,1), "h", 1, ("日・1時間経過", 13)),
                (False, ("日", 12,5,1), "m", 1, ("日・1分経過", 6)),
                (False, ("日", 12,5,1), "s", 1, ("日・1秒経過", 2)),
                ]
        def _checkcode(vals, f, v, expect):
            tmp = Time(*vals)
            if f == "h":
                tmp1 = tmp.elapsedHour(v)
                self.assertEqual(tmp1.name, expect[0])
                self.assertEqual(tmp1.hour, expect[1])
            elif f == "m":
                tmp1 = tmp.elapsedMin(v)
                self.assertEqual(tmp1.name, expect[0])
                self.assertEqual(tmp1.minute, expect[1])
            else:
                tmp1 = tmp.elapsedSec(v)
                self.assertEqual(tmp1.name, expect[0])
                self.assertEqual(tmp1.second, expect[1])
        validatedTestingWithFail(self, "methods", _checkcode, data)
