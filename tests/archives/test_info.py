# -*- coding: utf-8 -*-
"""Test: info.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import info as inf


_FILENAME = "info.py"


class InfoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Info class")

    def test_attributes(self):
        data = [
                ("test",
                    inf.Info._NAME, "test"),
                ]

        for v, exp_name, exp_note in data:
            tmp = inf.Info(v)
            self.assertIsInstance(tmp, inf.Info)
            self.assertEqual(tmp.name, exp_name)
            self.assertEqual(tmp.note, exp_note)

    def test_convert_flag_deflag(self):
        data = [
                ("test", True, inf.Flag, "test"),
                ("test", False, inf.Deflag, "test"),
                ]

        for v, isflg, exp_cls, expected in data:
            with self.subTest(v=v, isflg=isflg, exp_cls=exp_cls, expected=expected):
                tmp = inf.Info(v)
                res = tmp.flag() if isflg else tmp.deflag()
                self.assertIsInstance(res, exp_cls)
                self.assertEqual(res.note, expected)


class FlagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Flag class")

    def test_attributes(self):
        data = [
                ("test",
                    "test")
                ]

        for v, expected in data:
            tmp = inf.Flag(v)
            self.assertIsInstance(tmp, inf.Flag)
            self.assertEqual(tmp.note, expected)


class DeflagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Deflag class")

    def test_attributes(self):
        data = [
                ("test",
                    "test")
                ]

        for v, expected in data:
            tmp = inf.Deflag(v)
            self.assertIsInstance(tmp, inf.Deflag)
            self.assertEqual(tmp.note, expected)


class NothingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Nothing")

    def test_attributes(self):
        data = [
                (inf.Nothing._NAME, ""),
                ]
        for exp_name, exp_note in data:
            with self.subTest(exp_name=exp_name, exp_note=exp_note):
                tmp = inf.Nothing()
                self.assertIsInstance(tmp, inf.Nothing)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)


class SomethingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Something")

    def test_attributes(self):
        data = [
                (inf.Something._NAME, ""),
                ]

        for exp_name, exp_note in data:
            with self.subTest(exp_name=exp_name, exp_note=exp_note):
                tmp = inf.Something()
                self.assertIsInstance(tmp, inf.Something)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)
