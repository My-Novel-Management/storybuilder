# -*- coding: utf-8 -*-
"""Test: scene.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.day import Day
from builder.person import Person
from builder.scene import Scene
from builder.stage import Stage
from builder.time import Time
from builder.when import When
from builder.where import Where
from builder.who import Who


_FILENAME = "scene.py"


class SceneTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Scene class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("camera", "stage", "day", "time", "actions", "note")
        p1 = Person("Taro", "", 15, "male", "student")
        st1 = Stage("room")
        dy1 = Day("a day")
        tm1 = Time("night", 22,0,0)
        data = [
                (False, p1, st1, dy1, tm1,
                    (p1, st1, dy1, tm1, (), "")),
                ]
        def _creator(c, s, d, t):
            title = "test"
            data = ()
            if c and s and d and t:
                return Scene(title, data, camera=c, stage=s, day=d, time=t)
            elif c and s and d:
                return Scene(title, data, camera=c, stage=s, day=d)
            elif c and s:
                return Scene(title, data,camera=c, stage=s)
            else:
                return Scene(title, data)
        def _checkcode(camera, stage, day, time, expects):
            tmp = _creator(camera, stage, day, time)
            self.assertIsInstance(tmp, Scene)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

