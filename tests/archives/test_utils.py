# -*- coding: utf-8 -*-
"""Test for sbutils.py
"""
import unittest
import builder.sbutils as utl


class PublicMethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        utl.print_test_title("sbutils.py", "public methods")

    def test_assert_isbetween(self):
        data = [
                (10, 1, 5),
                ]

        for max_, min_, v in data:
            with self.subTest(max_=max_, min_=min_, v=v):
                self.assertTrue(utl.assert_isbetween(v, max_, min_))

    def test_assert_isbool(self):
        data = [
                (True, True)
                ]
        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.assert_isbool(v), expected)

    def test_assert_isclass(self):
        class Sample(object):
            def __init__(self, na):
                self.na = na

        data = [
                (Sample("test"), Sample),
                (("test",), tuple)
                ]

        for v, t in data:
            with self.subTest(v=v, t=t):
                self.assertTrue(utl.assert_isclass(v, t))

    def test_assert_isdict(self):
        data = [
                ({"a": "test"}, True),
                ]
        
        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.assert_isdict(v), expected)

    def test_assert_isint(self):
        data = [
                1,
                2,
                ]

        for v in data:
            with self.subTest(v=v):
                self.assertTrue(utl.assert_isint(v))

    def test_assert_islist(self):
        data = [
                ([1,2,3], True),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.assert_islist(v), expected)

    def test_assert_isobject(self):
        class Sample(object):
            def __init__(self, name):
                self.name = name

        data = [
                (Sample("test"), True),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.assert_isobject(v), expected)

    def test_assert_isstr(self):
        data = [
                "test",
                "list",
                ]

        for v in data:
            with self.subTest(v=v):
                self.assertTrue(utl.assert_isstr(v))

    def test_assert_istuple(self):
        data = [
                ((1,2,3), True),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(utl.assert_istuple(v), expected)

