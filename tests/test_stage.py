# -*- coding: utf-8 -*-
"""Test: stage.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.area import Area
from builder.stage import Stage


_FILENAME = "stage.py"


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Stage class")

    def setUp(self):
        pass

    def test_attributes(self):
        data = [
                (False, "test", "Tokyo", "a stage",
                    ("Tokyo", "a stage")),
                ]
        def _creator(name, area, info):
            if info:
                return Stage(name, area, info)
            elif area:
                return Stage(name, area)
            else:
                return Stage(name)
        def _checkcode(name, area, info, expect):
            tmp = _creator(name, area, info)
            self.assertIsInstance(tmp, Stage)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.data, expect)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

