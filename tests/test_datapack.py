# -*- coding: utf-8 -*-
"""Test: datapack.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.datapack import DataPack, titlePacked


_FILENAME = "datapack.py"


class DataPackTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "DataPack type and methods")

    def setUp(self):
        pass

    def test_attributes(self):
        data = [
                (False, "test", "a test",
                    DataPack("test", "a test")),
                ]
        def _checkcode(v1, v2, expect):
            tmp = DataPack(v1, v2)
            self.assertIsInstance(tmp, DataPack)
            self.assertEqual(tmp, expect)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_titlePacked(self):
        from builder.chapter import Chapter
        from builder.episode import Episode
        from builder.scene import Scene
        from builder.story import Story
        data = [
                (False, Story("test"),
                    DataPack("story title", "test")),
                (False, Chapter("test"),
                    DataPack("chapter title", "test")),
                (False, Episode("test"),
                    DataPack("episode title", "test")),
                (False, Scene("test"),
                    DataPack("scene title", "test")),
                ]
        def _checkcode(v, expect):
            tmp = titlePacked(v)
            self.assertEqual(tmp, expect)
        validatedTestingWithFail(self, "titlePacked", _checkcode, data)
