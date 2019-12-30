# -*- coding: utf-8 -*-
"""Test: checker.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType
from builder.action import Action
from builder.checker import Checker
from builder.chapter import Chapter
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene
from builder.story import Story


_FILENAME = "checkere.py"


class CheckerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Checker class")

    def setUp(self):
        self.taro = Person("Taro", "", 15, "male", "student")

    def test_attributes(self):
        tmp = Checker(Story("test"))
        self.assertIsInstance(tmp, Checker)

    def test_objectInOut(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1", Action("1",subject=self.taro, act_type=ActType.BE,note="1"),
                        Action("b",subject=self.taro, act_type=ActType.ACT))))),
                    True),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Checker(v).objectInOut(), expect)
        validatedTestingWithFail(self, "objectInOut", _checkcode, data)
