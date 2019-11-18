# -*- coding: utf-8 -*-
"""Test: action.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import assertion


_FILENAME = "assertion.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "assertion utility")

    def test_is_between(self):
        data = [
                (False, 10, 100, 1, 10,),
                (True, -1, 100, 1, 10,),
                (True, 100, 50, 1, 100,),
                ]
        validated_testing_withfail(self, "is_between",
                lambda v,mx,mn, expect: self.assertEqual(
                    assertion.is_between(v, mx, mn), expect), data)

    def test_is_bool(self):
        data = [
                (False, True, True,),
                (False, False, False,),
                (True, ["test"], True,),
                ]
        validated_testing_withfail(self, "is_bool",
                lambda v, expect: self.assertEqual(
                    assertion.is_bool(v), expect), data)

    def test_is_dict(self):
        data = [
                (False, {"test": "1"}, {"test": "1"},),
                (True, ["test", "1"], ["test", "1"],),
                ]
        validated_testing_withfail(self, "is_dict",
                lambda v, expect: self.assertEqual(
                    assertion.is_dict(v), expect), data)

    def test_is_instance(self):
        class Taro(object):
            def __init__(self, name: str):
                self._name = name
        class Hanako(object):
            def __init__(self, name: str):
                self._name = name
        taro1 = Taro("taro")
        data = [
                (False, taro1, Taro, taro1,),
                (True, taro1, Hanako, taro1,),
                ]
        validated_testing_withfail(self, "is_instance",
                lambda v,cls,expect: self.assertEqual(
                    assertion.is_instance(v, cls), expect), data)

    def test_is_int(self):
        data = [
                (False, 1, 1,),
                (True, "1", "1",),
                ]
        validated_testing_withfail(self, "is_int",
                lambda v, expect: self.assertEqual(
                    assertion.is_int(v), expect), data)

    def test_is_int_or_str(self):
        data = [
                (False, 1, 1,),
                (False, "1", "1",),
                (True, [1, 2], [1, 2],),
                ]
        validated_testing_withfail(self, "is_int_or_str",
                lambda v,expect: self.assertEqual(
                    assertion.is_int_or_str(v), expect), data)

    def test_is_list(self):
        data = [
                (False, [1,2,3], True, [1,2,3],),
                (False, (1,2,3), False, (1,2,3),),
                (True, (1,2,3), True, (1,2,3),),
                ]
        validated_testing_withfail(self, "is_list",
                lambda v,strict,expect: self.assertEqual(
                    assertion.is_list(v, strict), expect), data)

    def test_is_str(self):
        data = [
                (False, "1", "1",),
                (True, 1, 1,),
                ]
        validated_testing_withfail(self, "is_str",
                lambda v,expect: self.assertEqual(
                    assertion.is_str(v), expect), data)

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
                (False, taro1, Taro, taro1,),
                (False, hanako1, Taro, hanako1,),
                (True, taro1, Hanako, taro1,),
                ]
        validated_testing_withfail(self, "is_subclass",
                lambda v,cls,expect: self.assertEqual(
                    assertion.is_subclass(v,cls), expect), data)

    def test_is_tuple(self):
        data = [
                (False, (1,2,3), (1,2,3),),
                (True, [1,2,3], [1,2,3],),
                ]
        validated_testing_withfail(self, "is_tuple",
                lambda v,expect: self.assertEqual(
                    assertion.is_tuple(v), expect), data)
