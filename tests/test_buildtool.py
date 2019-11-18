# -*- coding: utf-8 -*-
"""Test: buildtool.py
"""
import unittest
from testutils import print_test_title
from builder.buildtool import Build
from builder.story import Story
from builder.world import World

_FILENAME = "buildtool.py"


class BuildTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Build class")

    def test_attributes(self):
        tmp = Build(Story("test"), World(), is_debug_test=True)
        self.assertIsInstance(tmp, Build)

    @unittest.skip("integration test")
    def test_output_story(self):
        pass

    @unittest.skip("integration test")
    def test_to_analyzed_info(self):
        pass

    @unittest.skip("integration test")
    def test_to_description(self):
        pass

    @unittest.skip("integration test")
    def test_to_detail_info(self):
        pass

    @unittest.skip("integration test")
    def test_to_digalogue(self):
        pass

    @unittest.skip("integration test")
    def test_to_layer(self):
        pass

    @unittest.skip("integration test")
    def test_to_outline(self):
        pass

    @unittest.skip("integration test")
    def test_to_scenario(self):
        pass

    @unittest.skip("integration test")
    def test_to_total_info(self):
        pass
