# -*- coding: utf-8 -*-
"""Test: assertion.py
"""
import unittest
from builder.testutils import print_test_title
from builder import assertion as ast

_FILENAME = "assertion.py"


class PublicMethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "public methods")

    def test_is_between(self):
        data = [
                (1, 10, 0, True, 1),
                (5, 3, 0, False, 5),
                (5, 100, 10, False, 5),
                ]

        for v, max, min, isfail, expected in data:
            with self.subTest(v=v, max=max, min=min, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_between(v, max, min), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_between(v, max, min), expected)

    def test_is_bool(self):
        data = [
                (True, True, True),
                (False, True, False),
                (1, False, 1),
                ]

        for v, isfail, expected in data:
            with self.subTest(v=v, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_bool(v), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_bool(v), expected)

    def test_is_dict(self):
        data = [
                ({"t":"test"}, True, {"t":"test"}),
                (["test"], False, ["test"]),
                ]

        for v, isfail, expected in data:
            with self.subTest(v=v, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_dict(v), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_dict(v), expected)

    def test_is_instance(self):
        class Sample(object):
            def __init__(self, name):
                self.name = name

        class NoSample(object):
            def __init__(self, note):
                self.note = note

        data = [
                (Sample("test"), Sample, True, "test"),
                (NoSample("test"), Sample, False, None),
                ]

        for v, scls, isfail, expected in data:
            with self.subTest(v=v, scls=scls, isfail=isfail, expected=expected):
                if isfail:
                    self.assertIsInstance(ast.is_instance(v, scls), scls)
                    self.assertEqual(ast.is_instance(v, scls).name, expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertNotIsInstance(ast.is_instance(v, scls), scls)

    def test_is_int(self):
        data = [
                (1, True, 1),
                ("1", False, "1"),
                ]

        for v, isfail, expected in data:
            with self.subTest(v=v, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_int(v), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_int(v), expected)

    def test_is_int_or_str(self):
        data = [
                (1, True, 1),
                ("1", True, "1"),
                (["test"], False, ["test"]),
                ]

        for v, isfail, expected in data:
            with self.subTest(v=v, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_int_or_str(v), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_int_or_str(v), expected)

    def test_is_list(self):
        data = [
                (["test"], True, True, ["test"]),
                (("test",), True, False, ("test",)),
                (("test",), False, True, ("test",)),
                ]

        for v, strict, isfail, expected in data:
            with self.subTest(v=v, strict=strict, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_list(v, strict), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_list(v, strict), expected)

    def test_is_str(self):
        data = [
                ("test", True, "test"),
                (1, False, 1),
                ]

        for v, isfail, expected in data:
            with self.subTest(v=v, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_str(v), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_str(v), expected)

    def test_is_subclass(self):
        class BaseSample(object):
            def __init__(self, name):
                self.name = name

        class Sample(BaseSample):
            def __init__(self, name):
                super().__init__(name)

        class TestSample(object):
            def __init__(self, name):
                self.name = name

        data = [
                (Sample, BaseSample, True, Sample),
                (BaseSample, TestSample, False, BaseSample),
                ]

        for v, scls, isfail, expected in data:
            with self.subTest(v=v, scls=scls, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_subclass(v, scls), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_subclass(v, scls), expected)

    def test_is_tuple(self):
        data = [
                (("test",), True, ("test",)),
                (["test"], False, ["test"]),
                ]

        for v ,isfail, expected in data:
            with self.subTest(v=v, isfail=isfail, expected=expected):
                if isfail:
                    self.assertEqual(ast.is_tuple(v), expected)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(ast.is_tuple(v), expected)

