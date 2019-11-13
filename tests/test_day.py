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
        d = dy.Day("test day", 10, 7, 2019)
        self.assertIsInstance(d, dy.Day)
        self.assertEqual(d.year, 2019)
        self.assertEqual(d.mon, 10)
        self.assertEqual(d.day, 7)

