# -*- coding: utf-8 -*-
"""Test: time.py
"""
## public libs
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
                    (12, 1, 5, "a time")),
                ]
        def _creator(name, hour, min, sec, note):
            if hour and min and sec and note:
                return Time(name, hour, min, sec, note)
            elif hour and min and sec:
                return Time(name, hour, min, sec)
            elif hour and min:
                return Time(name, hour, min)
            elif hour:
                return Time(name, hour)
            else:
                return Time(name)
        def _checkcode(name, hour, min, sec, note, expects):
            tmp = _creator(name, hour, min, sec, note)
            self.assertIsInstance(tmp, Time)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

