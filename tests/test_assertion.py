# -*- coding: utf-8 -*-
"""Test: action.py
"""
import unittest
from testutils import print_test_title
from builder import assertion


_FILENAME = "assertion.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "assertion utility")

    def test_is_between(self):
        data = [
                (10, 100, 1, 10, False),
                (100, 50, 1, 100, True),
                ]
        for v, mx, mn, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_between(v, mx, mn), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_between(v, mx, mn), expect)

    def test_is_bool(self):
        data = [
                (True, True, False),
                (False, False, False),
                (["test"], True, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_bool(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_bool(v), expect)

    def test_is_dict(self):
        data = [
                ({"test": "1"}, {"test": "1"}, False),
                (["test", "1"], ["test", "1"], True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_dict(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_dict(v), expect)

    def test_is_instance(self):
        class Taro(object):
            def __init__(self, name: str):
                self._name = name
        class Hanako(object):
            def __init__(self, name: str):
                self._name = name
        taro1 = Taro("taro")
        data = [
                (taro1, Taro, taro1, False),
                (taro1, Hanako, taro1, True),
                ]
        for v, cls, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_instance(v, cls), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_instance(v, cls), expect)

    def test_is_int(self):
        data = [
                (1, 1, False),
                ("1", "1", True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_int(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_int(v), expect)

    def test_is_int_or_str(self):
        data = [
                (1, 1, False),
                ("1", "1", False),
                ([1, 2], [1, 2], True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_int_or_str(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_int_or_str(v), expect)

    def test_is_list(self):
        data = [
                ([1,2,3], True, [1,2,3], False),
                ((1,2,3), True, (1,2,3), True),
                ]
        for v, strict, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_list(v, strict), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_list(v, strict), expect)

    def test_is_str(self):
        data = [
                ("1", "1", False),
                (1, 1, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_str(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_str(v), expect)

    def test_is_subclass(self):
        class Taro(object):
            def __init__(self, name: str):
                self._name = name
        class Hanako(Taro):
            def __init__(self, name: str, age: int):
                super().__init__(name)
                self._age = age
        taro1 = Taro("taro")
        hanako1 = Hanako("hana", 1)
        data = [
                (taro1, Taro, taro1, False),
                (hanako1, Taro, hanako1, False),
                (taro1, Hanako, taro1, True),
                ]
        for v, cls, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_subclass(v, cls), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_subclass(v, cls), expect)

    def test_is_tuple(self):
        data = [
                ((1,2,3), (1,2,3), False),
                ([1,2,3], [1,2,3], True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    self.assertEqual(assertion.is_tuple(v), expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertEqual(assertion.is_tuple(v), expect)
