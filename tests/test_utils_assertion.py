# -*- coding: utf-8 -*-
"""Test: assertion.py
"""
import unittest
from testutils import printTestTitle, validatedTestingWithFail
from utils import assertion


_FILENAME = "assertion.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "assertion utility")

    def test_hasKey(self):
        data = [
                (False, "k", {"k":1,"d":2},
                    1),
                (True, "a", {"k":1,"d":2},
                    1),
                ]
        validatedTestingWithFail(self, "hasKey",
                lambda k,v,expect: self.assertEqual(assertion.hasKey(k,v), expect), data)

    def test_isBetween(self):
        data = [
                (False, 10, 100, 1, 10,),
                (True, -1, 100, 1, 10,),
                (True, 100, 50, 1, 100,),
                ]
        validatedTestingWithFail(self, "isBetween",
                lambda v,mx,mn, expect: self.assertEqual(
                    assertion.isBetween(v, mx, mn), expect), data)

    def test_isBool(self):
        data = [
                (False, True, True,),
                (False, False, False,),
                (True, ["test"], True,),
                ]
        validatedTestingWithFail(self, "isBool",
                lambda v, expect: self.assertEqual(
                    assertion.isBool(v), expect), data)

    def test_isDict(self):
        data = [
                (False, {"test": "1"}, {"test": "1"},),
                (True, ["test", "1"], ["test", "1"],),
                ]
        validatedTestingWithFail(self, "isDict",
                lambda v, expect: self.assertEqual(
                    assertion.isDict(v), expect), data)

    def test_isInstance(self):
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
        validatedTestingWithFail(self, "isInstance",
                lambda v,cls,expect: self.assertEqual(
                    assertion.isInstance(v, cls), expect), data)

    def test_isInt(self):
        data = [
                (False, 1, 1,),
                (True, "1", "1",),
                ]
        validatedTestingWithFail(self, "isInt",
                lambda v, expect: self.assertEqual(
                    assertion.isInt(v), expect), data)

    def test_isIntOrStr(self):
        data = [
                (False, 1, 1,),
                (False, "1", "1",),
                (True, [1, 2], [1, 2],),
                ]
        validatedTestingWithFail(self, "isIntOrStr",
                lambda v,expect: self.assertEqual(
                    assertion.isIntOrStr(v), expect), data)

    def test_isList(self):
        data = [
                (False, [1,2,3], True, [1,2,3],),
                (False, (1,2,3), False, (1,2,3),),
                (True, (1,2,3), True, (1,2,3),),
                ]
        validatedTestingWithFail(self, "isList",
                lambda v,strict,expect: self.assertEqual(
                    assertion.isList(v, strict), expect), data)

    def test_isStr(self):
        data = [
                (False, "1", "1",),
                (True, 1, 1,),
                ]
        validatedTestingWithFail(self, "isStr",
                lambda v,expect: self.assertEqual(
                    assertion.isStr(v), expect), data)

    def test_isSubclass(self):
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
        validatedTestingWithFail(self, "isSubclass",
                lambda v,cls,expect: self.assertEqual(
                    assertion.isSubclass(v,cls), expect), data)

    def test_isTuple(self):
        data = [
                (False, (1,2,3), (1,2,3),),
                (True, [1,2,3], [1,2,3],),
                ]
        validatedTestingWithFail(self, "isTuple",
                lambda v,expect: self.assertEqual(
                    assertion.isTuple(v), expect), data)
