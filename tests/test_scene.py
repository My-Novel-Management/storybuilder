# -*- coding: utf-8 -*-
"""Test: scene.py
"""
import unittest
from testutils import print_test_title
from builder import scene as sc
from builder.action import Action
from builder.person import Person
from builder.stage import Stage
from builder.day import Day
from builder.time import Time


_FILENAME = "scene.py"


class SceneTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Scene class")

    def setUp(self):
        self.taro = Person("Taro", "", 10, "male", "student")
        act1 = Action(self.taro, "test")
        self.scene1 = sc.Scene("test", "a test", act1)

    def test_attributes(self):
        taro = Person("Taro", "", 10, "male", "student")
        act1 = Action(taro, "test")
        room = Stage("Room", "a room")
        day1 = Day("day1", 10,1,2019)
        time1 = Time("morning", 8,0)
        data = [
                ("test", "a test", (act1,),
                    taro, room, day1, time1, False),
                ]
        for title, outline, acts, camera, stage, day, time, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = sc.Scene(title, outline, *acts,
                            camera=camera, stage=stage,
                            day=day, time=time)
                    self.assertIsInstance(tmp, sc.Scene)
                    self.assertEqual(tmp.title, title)
                    self.assertEqual(tmp.outline, outline)
                    self.assertEqual(tmp.camera, camera)
                    self.assertEqual(tmp.stage, stage)
                    self.assertEqual(tmp.day, day)
                    self.assertEqual(tmp.time, time)
                    self.assertEqual(tmp.actions, acts)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = sc.Scene(title, outline, args,
                                camera=camera, stage=stage,
                                day=day, time=time)
                        self.assertIsInstance(tmp, sc.Scene)
                        self.assertEqual(tmp.title, title)
                        self.assertEqual(tmp.outline, outline)
                        self.assertEqual(tmp.camera, camera)
                        self.assertEqual(tmp.stage, stage)
                        self.assertEqual(tmp.day, day)
                        self.assertEqual(tmp.time, time)
                        self.assertEqual(tmp.actions, acts)

    def test_inherited(self):
        taro = Person("Taro", "", 10, "male", "student")
        act1 = Action(taro, "test")
        data = [
                ("apple", "an apple", (act1,), False),
                ]
        for title, outline, acts, isfail in data:
            with self.subTest(title=title):
                tmp = sc.Scene(title, outline)
                if not isfail:
                    tmp1 = tmp.inherited(*acts)
                    self.assertIsInstance(tmp1, sc.Scene)
                    self.assertEqual(tmp1.title, title)
                    self.assertEqual(tmp1.outline, outline)
                    self.assertEqual(tmp1.actions, acts)
                else:
                    with self.assertRaises(AssertionError):
                        tmp1 = tmp.inherited(*acts)
                        self.assertIsInstance(tmp1, sc.Scene)
                        self.assertEqual(tmp1.title, title)
                        self.assertEqual(tmp1.outline, outline)
                        self.assertEqual(tmp1.actions, acts)

    def test_setCamera(self):
        data = [
                (Person("hana", "", 17, "female", "girl"), False),
                ]
        for camera, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = self.scene1.setCamera(camera)
                    self.assertIsInstance(tmp, sc.Scene)
                    self.assertEqual(tmp.camera, camera)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = self.scene1.setCamera(camera)
                        self.assertIsInstance(tmp, sc.Scene)
                        self.assertEqual(tmp.camera, camera)

    def test_setStage(self):
        data = [
                (Stage("room", "a test"), False),
                ]
        for stage, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = self.scene1.setStage(stage)
                    self.assertIsInstance(tmp, sc.Scene)
                    self.assertEqual(tmp.stage, stage)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = self.scene1.setStage(stage)
                        self.assertIsInstance(tmp, sc.Scene)
                        self.assertEqual(tmp.stage, stage)

    def test_setDay(self):
        data = [
                (Day("test day", 5,9, 2020), False),
                ]
        for day, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = self.scene1.setDay(day)
                    self.assertIsInstance(tmp, sc.Scene)
                    self.assertEqual(tmp.day, day)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = self.scene1.setDay(day)
                        self.assertIsInstance(tmp, sc.Scene)
                        self.assertEqual(tmp.day, day)

    def test_setTime(self):
        data = [
                (Time("night", 20,10, 2020), False),
                ]
        for time, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = self.scene1.setTime(time)
                    self.assertIsInstance(tmp, sc.Scene)
                    self.assertEqual(tmp.time, time)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = self.scene1.setTime(time)
                        self.assertIsInstance(tmp, sc.Scene)
                        self.assertEqual(tmp.time, time)

    def test_add(self):
        act1 = Action(self.taro, "apple")
        act2 = Action(self.taro, "orange")
        data = [
                ((act1,), (act1,), False),
                ((act1, act2), (act1, act2), False),
                ((self.taro,), (self.taro,), True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                tmp = self.scene1.inherited()
                if not isfail:
                    tmp.add(*v)
                    self.assertEqual(tmp.actions, expect)
                else:
                    with self.assertRaises(AssertionError):
                        tmp.add(*v)
                        self.assertEqual(tmp.actions, expect)
