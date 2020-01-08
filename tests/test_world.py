# -*- coding: utf-8 -*-
"""Test: world.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.block import Block
from builder.chapter import Chapter
from builder.episode import Episode
from builder.scene import Scene
from builder.world import World


_FILENAME = "world.py"


class WorldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "World class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = World("test")
        self.assertIsInstance(tmp, World)

    def test_entryBlock(self):
        tmp = World("test")
        self.assertTrue(tmp.entryBlock(tmp.block("apple")))

    def test_setPersons(self):
        tmp = World("test")
        tmp.setPersons(
                [["taro", "Taro", "", 15, (1,1), "male", "student"],]
                )
        self.assertTrue(hasattr(tmp, "taro"))

    def test_setStages(self):
        tmp = World("test")
        tmp.setStages(
                [["room", "Room", "a room", ""]]
                )
        self.assertTrue(hasattr(tmp, "on_room"))
        self.assertTrue(hasattr(tmp, "on_room_int"))
        self.assertTrue(hasattr(tmp, "on_room_ext"))

    def test_setItems(self):
        tmp = World("test")
        tmp.setItems(
                [["apple", "Apple", ""]]
                )
        self.assertTrue(hasattr(tmp, "apple"))

    def test_setDays(self):
        tmp = World("test")
        tmp.setDays(
                [["day1", "Day1", 1,1, 2020]]
                )
        self.assertTrue(hasattr(tmp, "in_day1"))

    def test_setTimes(self):
        tmp = World("test")
        tmp.setTimes(
                [["time1", "Time", 12,0,0]]
                )
        self.assertTrue(hasattr(tmp, "at_time1"))

    def teset_setWords(self):
        tmp = World("test")
        tmp.setWords(
                [["orange", "Orange"]]
                )
        self.assertTrue(hasattr(tmp, "w_orange"))

    def test_setRubis(self):
        tmp = World("test")
        tmp.setRubis(
                [["桃太郎", "｜桃太郎《ももたろう》", "", 1]]
                )
        self.assertTrue("桃太郎" in tmp.rubis)

    def test_setLayers(self):
        tmp = World("test")
        tmp.setLayers(
                [["test", "テスト", ("test",)]]
                )
        self.assertTrue("test" in tmp.layers)

    def test_setStageLayers(self):
        tmp = World("test")
        tmp.setStageLayers(
                [["test", "テスト", ("test",)]]
                )
        self.assertTrue("test" in tmp.stagelayers)

    def test_setDayTimeLayers(self):
        tmp = World("test")
        tmp.setDayTimeLayers(
                [["test", "テスト", ("test",)]]
                )
        self.assertTrue("test" in tmp.daytimes)

    def test_setFashionLayers(self):
        tmp = World("test")
        tmp.setFashionLayers(
                [["test", "テスト", ("test",)]]
                )
        self.assertTrue("test" in tmp.fashionlayers)

    def test_setFoodLayers(self):
        tmp = World("test")
        tmp.setFoodLayers(
                [["test", "テスト", ("test",)]]
                )
        self.assertTrue("test" in tmp.foodlayers)

    def test_block(self):
        tmp = World("test")
        self.assertIsInstance(tmp.block("test"), Block)

    def test_chapter(self):
        tmp = World("test")
        self.assertIsInstance(tmp.chapter("test"), Chapter)

    def test_episode(self):
        tmp = World("test")
        self.assertIsInstance(tmp.episode("test"), Episode)

    def test_load(self):
        tmp = World("test")
        tmp.entryBlock(tmp.block("test"))
        self.assertIsInstance(tmp.load("test"), Block)

    def test_scene(self):
        tmp = World("test")
        self.assertIsInstance(tmp.scene("test"), Scene)

    def tset_br(self):
        tmp = World("test")
        self.assertIsInstance(tmp.br(), Action)

    def test_comment(self):
        tmp = World("test")
        self.assertIsInstance(tmp.comment("test"), Action)

    def test_symbol(self):
        tmp = World("test")
        self.assertIsInstance(tmp.symbol("!"), Action)
