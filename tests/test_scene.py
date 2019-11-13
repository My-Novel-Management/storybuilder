# -*- coding: utf-8 -*-
"""Test: scene.py
"""
import unittest
from testutils import print_test_title
from builder import scene as sc

_FILENAME = "scene.py"


class SceneTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Scene class")

    def test_attributes(self):
        s = sc.Scene("test title", "outline")
        self.assertTrue(isinstance(s, sc.Scene))
        self.assertEqual(s.title, "test title")
        self.assertEqual(s.outline, "outline")

    def test_method_setCamera(self):
        s = sc.Scene("test scene", "outline")
        pass

    def test_method_setStage(self):
        s = sc.Scene("test scene", "outline")
        st = sc.Stage("test stage", "a room")
        s.setStage(st)
        self.assertIsInstance(s.stage, sc.Stage)

    def test_method_setDay(self):
        s = sc.Scene("test scene", "outline")
        dy = sc.Day("test day", 10,10, 2019)
        s.setDay(dy)
        self.assertIsInstance(s.day, sc.Day)

    def test_method_setTime(self):
        s = sc.Scene("test scene", "outline")
        tm = sc.Time("test time", 12,30)
        s.setTime(tm)
        self.assertIsInstance(s.time, sc.Time)
