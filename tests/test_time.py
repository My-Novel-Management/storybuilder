# -*- coding: utf-8 -*-
"""Test: time.py
"""
import unittest
from testutils import print_test_title
from builder import time as tm


_FILENAME = "time.py"


class TimeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Time class")

    def test_attributes(self):
        t = tm.Time("test time", 12, 30, 10)
        self.assertIsInstance(t, tm.Time)
        self.assertEqual(t.hour, 12)
        self.assertEqual(t.min, 30)
        self.assertEqual(t.sec, 10)
        self.assertEqual(t.numsys, tm.Time.DEF_NUMSYS)

