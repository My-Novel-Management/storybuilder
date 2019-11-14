# -*- coding: utf-8 -*-
"""Test: basesubject.py
"""
import unittest
from testutils import print_test_title
from builder import basesubject as bs


_FILENAME = "basesubject.py"


class BaseSubjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseSubject class")

    def test_attributes(self):
        tmp = bs.BaseSubject("test")
        self.assertIsInstance(tmp, bs.BaseSubject)
        self.assertEqual(tmp.name, "test")

class NoSubjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "NoSubject class")

    def test_attributes(self):
        tmp = bs.NoSubject()
        self.assertIsInstance(tmp, bs.NoSubject)
        self.assertEqual(tmp.name, bs.NoSubject.__NAME__)
