# -*- coding: utf-8 -*-
'''
Custom assertion methods test
=============================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.utils import assertion


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(assertion.__name__, 'custom assertion methods')

    def test_is_between(self):
        data = [
                # (val, max, min, expect)
                (True, 10, 100, 1, 10,),
                (False, -1, 100, 1, 10,),
                (False, 100, 50, 1, 100,),
                ]
        validate_with_fail(self, "is_between",
            lambda v,mx,mn,expect: self.assertEqual(assertion.is_between(v, mx, mn), expect),
                data)

    def test_is_bool(self):
        data = [
                # (val, expect)
                (True, True, True,),
                (True, False, False,),
                (False, ["test"], True,),
                ]
        validate_with_fail(self, "is_bool",
            lambda v,expect: self.assertEqual(assertion.is_bool(v), expect), data)

    def test_is_dict(self):
        data = [
                # (val, expect)
                (True, {"test": "1"}, {"test": "1"},),
                (False, ["test", "1"], ["test", "1"],),
                ]
        validate_with_fail(self, "is_dict",
            lambda v,expect: self.assertEqual(assertion.is_dict(v), expect), data)

    def test_is_instance(self):
        class Taro(object):
            def __init__(self, name: str):
                self._name = name
        class Hanako(object):
            def __init__(self, name: str):
                self._name = name
        taro1 = Taro("taro")
        data = [
                # (val, class, expect)
                (True, taro1, Taro, taro1,),
                (False, taro1, Hanako, taro1,),
                ]
        validate_with_fail(self, "is_instance",
            lambda v,cls, expect: self.assertEqual(assertion.is_instance(v, cls), expect),
                data)

    def test_is_int(self):
        data = [
                # (val, expect)
                (True, 1, 1,),
                (False, "1", "1",),
                ]
        validate_with_fail(self, "is_int",
            lambda v,expect: self.assertEqual(assertion.is_int(v), expect), data)

    def test_is_int_or_float(self):
        data = [
                # (val, expect)
                (True, 1, 1,),
                (True, 1.1, 1.1,),
                (False, "1", "1",),
                ]
        validate_with_fail(self, "is_int_or_float",
            lambda v,expect: self.assertEqual(assertion.is_int_or_float(v), expect), data)


    def test_is_int_or_str(self):
        data = [
                # (val, expect)
                (True, 1, 1,),
                (True, "1", "1",),
                (False, [1, 2], [1, 2],),
                ]
        validate_with_fail(self, "is_int_or_str",
            lambda v,expect: self.assertEqual(assertion.is_int_or_str(v), expect),
                data)

    def test_is_list(self):
        data = [
                # (val, expect)
                (True, [1,2,3], [1,2,3],),
                (False, 1, 1),
                (False, (1,2), (1,2)),
                ]
        validate_with_fail(self, "is_list",
            lambda v,expect: self.assertEqual(assertion.is_list(v), expect),
                data)

    def test_is_listlike(self):
        data = [
                # (val, expect)
                (True, [1,2,3], [1,2,3]),
                (True, (1,2), (1,2)),
                (False, 1, 1),
                ]
        validate_with_fail(self, "is_listlike",
            lambda v,expect: self.assertEqual(assertion.is_listlike(v), expect),
                data)

    def test_is_str(self):
        data = [
                # (val, expect)
                (True, "1", "1",),
                (False, 1, 1,),
                ]
        validate_with_fail(self, "is_str",
            lambda v,expect: self.assertEqual(assertion.is_str(v), expect),
                data)

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
                # (val, class, expect)
                (True, taro1, Taro, taro1,),
                (True, hanako1, Taro, hanako1,),
                (False, taro1, Hanako, taro1,),
                ]
        validate_with_fail(self, "is_subclass",
            lambda v,cls, expect: self.assertEqual(assertion.is_subclass(v,cls), expect),
                data)

    def test_is_tuple(self):
        data = [
                # (val, expect)
                (True, (1,2,3), (1,2,3),),
                (False, 1, 1),
                (False, [1,2,3], [1,2,3],),
                ]
        validate_with_fail(self, "is_tuple",
            lambda v,expect: self.assertEqual(assertion.is_tuple(v), expect),
                data)

    def test_is_various_types(self):
        data = [
                # (val, types, expect)
                (True, 1, (int, str), 1),
                (True, "1", (int, str), "1"),
                (False, [1,2], (int, str), [1,2]),
                ]
        validate_with_fail(self, "is_various_types",
                lambda v,types,expect: self.assertEqual(
                    assertion.is_various_types(v,types), expect),
                    data)
