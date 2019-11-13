# -*- coding: utf-8 -*-
"""Test: world.py
"""
import unittest
from testutils import print_test_title
from builder import world as wd


_FILENAME = "world.py"


class UtilityDictTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "UtilityDict class")

    def test_attributes(self):
        tmp = wd.UtilityDict()
        tmp["test"] = "apple"
        self.assertTrue(hasattr(tmp, "test"))


class WorldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "World class")

    def test_instance(self):
        w = wd.World()
        self.assertIsInstance(w, wd.World)

    def test_attributes(self):
        w = wd.World()
        self.assertTrue(hasattr(w, "day"))
        self.assertTrue(hasattr(w, "item"))
        self.assertTrue(hasattr(w, "stage"))
        self.assertTrue(hasattr(w, "time"))
        self.assertTrue(hasattr(w, "word"))
        self.assertIsInstance(w.day, wd.UtilityDict)
        self.assertIsInstance(w.item, wd.UtilityDict)
        self.assertIsInstance(w.stage, wd.UtilityDict)
        self.assertIsInstance(w.time, wd.UtilityDict)
        self.assertIsInstance(w.word, wd.UtilityDict)

    def test_method_chapter(self):
        w = wd.World()
        res = w.chapter("test chapter")
        self.assertIsInstance(res, wd.Chapter)

    def test_method_append_day(self):
        w = wd.World()
        data = [
                ("day1", "test day", 10, 1, 2019),
                ]
        for tag, name, mon, day, year in data:
            with self.subTest(tag=tag, name=name, mon=mon, day=day, year=year):
                res = w.append_day(tag, (name, mon, day, year))
                self.assertTrue(hasattr(w.day, tag))
                self.assertIsInstance(w.day[tag], wd.Day)

    def test_method_append_item(self):
        w = wd.World()
        data = [
                ("item1", "test1", "testing"),
                ]
        for tag, name, note in data:
            with self.subTest(tag=tag, name=name, note=note):
                res = w.append_item(tag, (name, note))
                self.assertTrue(hasattr(w.item, tag))
                self.assertIsInstance(w.item[tag], wd.Item)
