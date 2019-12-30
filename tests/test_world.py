# -*- coding: utf-8 -*-
"""Test: world.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.world import World
from utils.utildict import UtilityDict


_FILENAME = "world.py"


class WorldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "World class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("title",
                "rubis", "layers")
        data = [
                (False, ("test",),
                    ("test",
                        {},{})),
                ]
        def _checkcode(vals, expects):
            tmp = World(*vals)
            self.assertIsInstance(tmp, World)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    ## methods of build
    def test_compileFiles(self):
        pass

    def test_buildDB(self):
        pass

    def test_buildStory(self):
        pass

    ## methods of scene
    def test_load(self):
        pass

    def test_scene(self):
        pass

    def test_create(self):
        pass

