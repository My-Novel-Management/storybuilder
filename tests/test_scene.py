# -*- coding: utf-8 -*-
"""Test: scene.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
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
                (False, "test", "a test", (act1,),
                    taro, room, day1, time1,),
                ]
        def _checkcode(title, outline, acts, camera, stage, day, time):
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
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        taro = Person("Taro", "", 10, "male", "student")
        act1 = Action(taro, "test")
        data = [
                (False, "apple", "an apple", (act1,),),
                ]
        def _checkcode(title, outline, acts):
            tmp = sc.Scene(title, outline)
            tmp1 = tmp.inherited(*acts)
            self.assertIsInstance(tmp1, sc.Scene)
            self.assertEqual(tmp1.title, title)
            self.assertEqual(tmp1.outline, outline)
            self.assertEqual(tmp1.actions, acts)
        validated_testing_withfail(self, "inherited", _checkcode, data)

    def test_setCamera(self):
        data = [
                (False, Person("hana", "", 17, "female", "girl"),),
                ]
        def _checkcode(camera):
            tmp = self.scene1.setCamera(camera)
            self.assertIsInstance(tmp, sc.Scene)
            self.assertEqual(tmp.camera, camera)
        validated_testing_withfail(self, "setCamera", _checkcode, data)

    def test_setStage(self):
        data = [
                (False, Stage("room", "a test"),),
                ]
        def _checkcode(stage):
            tmp = self.scene1.setStage(stage)
            self.assertIsInstance(tmp, sc.Scene)
            self.assertEqual(tmp.stage, stage)
        validated_testing_withfail(self, "setStage", _checkcode, data)

    def test_setDay(self):
        data = [
                (False, Day("test day", 5,9, 2020),),
                ]
        def _checkcode(day):
            tmp = self.scene1.setDay(day)
            self.assertIsInstance(tmp, sc.Scene)
            self.assertEqual(tmp.day, day)
        validated_testing_withfail(self, "setDay", _checkcode, data)

    def test_setTime(self):
        data = [
                (False, Time("night", 20,10, 2020),),
                ]
        def _checkcode(time):
            tmp = self.scene1.setTime(time)
            self.assertIsInstance(tmp, sc.Scene)
            self.assertEqual(tmp.time, time)
        validated_testing_withfail(self, "setTime", _checkcode, data)

    def test_add(self):
        act1 = Action(self.taro, "apple")
        act2 = Action(self.taro, "orange")
        data = [
                (False, (act1,), (act1,),),
                (False, (act1, act2), (act1, act2),),
                (True, (self.taro,), (self.taro,),),
                ]
        def _checkcode(v, expect):
            tmp = self.scene1.inherited()
            tmp.add(*v)
            self.assertEqual(tmp.actions, expect)
        validated_testing_withfail(self, "add", _checkcode, data)
