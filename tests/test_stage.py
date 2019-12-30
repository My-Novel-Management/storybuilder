# -*- coding: utf-8 -*-
"""Test: stage.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.stage import Stage


_FILENAME = "stage.py"


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Stage class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("note",)
        data = [
                (False, "test", "a stage",
                    ("a stage",)),
                ]
        def _creator(name, note):
            if note:
                return Stage(name, note)
            else:
                return Stage(name)
        def _checkcode(name, note, expects):
            tmp = _creator(name, note)
            self.assertIsInstance(tmp, Stage)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

