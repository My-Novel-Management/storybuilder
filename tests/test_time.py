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

