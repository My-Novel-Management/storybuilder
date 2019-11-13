# -*- coding: utf-8 -*-
"""Test for basesubject.py
"""
import unittest
from builder.testutils import print_test_title
from builder import basesubject as bs


_FILENAME = "basesubject.py"


class BaseSubjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseSubject")

    def test_attributes(self):
        data = [
                ("Taro", "a man",
                    "Taro", "a man"),
                ]

        for name, note, exp_name, exp_note in data:
            with self.subTest(name=name, note=note, exp_name=exp_name, exp_note=exp_note):
                tmp = bs.BaseSubject(name, note)
                self.assertIsInstance(tmp, bs.BaseSubject)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)
