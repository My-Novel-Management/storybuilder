# -*- coding: utf-8 -*-
"""Test: scene.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.action import Action
from builder.block import Block
from builder.day import Day
from builder.person import Person
from builder.pronoun import When, Where, Who
from builder.scene import Scene
from builder.stage import Stage
from builder.time import Time


_FILENAME = "scene.py"


class SceneTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Scene class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("camera", "stage", "day", "time", "data", "note")
        p1 = Person("Taro", "", 15, (1,1), "male", "student")
        st1 = Stage("room")
        dy1 = Day("a day")
        tm1 = Time("night", 22,0,0)
        data = [
                (False, p1, st1, dy1, tm1,
                    (p1, st1, dy1, tm1, (), "")),
                ]
        def _creator(c, s, d, t):
            title = "test"
            if c and s and d and t:
                return Scene(title, camera=c, stage=s, day=d, time=t)
            elif c and s and d:
                return Scene(title, camera=c, stage=s, day=d)
            elif c and s:
                return Scene(title, camera=c, stage=s)
            else:
                return Scene(title)
        def _checkcode(camera, stage, day, time, expects):
            tmp = _creator(camera, stage, day, time)
            self.assertIsInstance(tmp, Scene)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_attributes2(self):
        ac1, ac2 = Action("apple"), Action("orange")
        bk1, bk2 = Block("A"), Block("B")
        data = [
                (False, (ac1,ac2),
                    (ac1,ac2)),
                (False, (bk1, bk2),
                    (bk1, bk2)),
                (False, (ac1, bk1),
                    (ac1, bk1)),
                ]
        def _checkcode(vals, expect):
            tmp = Scene("test", *vals)
            self.assertEqual(tmp.data, expect)
        validatedTestingWithFail(self, "class attributes(Action, Scene)", _checkcode, data)

    def test_inherited(self):
        ac1, ac2 = Action("apple"), Action("orange")
        tmp = Scene("test", ac1)
        self.assertEqual(tmp.data, (ac1,))
        tmp1 = tmp.inherited(ac2)
        self.assertEqual(tmp1.data, (ac2,))
