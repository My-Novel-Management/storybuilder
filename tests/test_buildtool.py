# -*- coding: utf-8 -*-
"""Test: buildtool.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.buildtool import Build


_FILENAME = "buildtool.py"


class BuildTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Build class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = Build("test")
        self.assertIsInstance(tmp, Build)

