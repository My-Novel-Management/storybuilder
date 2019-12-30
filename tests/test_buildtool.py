# -*- coding: utf-8 -*-
"""Test: buildtool.py
"""
## public libs
import datetime
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.buildtool import Build
from builder.story import Story


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
        self.assertIsInstance(tmp.date, datetime.date)

    def test_output(self):
        pass
