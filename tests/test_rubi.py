# -*- coding: utf-8 -*-
"""Test: rubi.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.rubi import Rubi


_FILENAME = "rubi.py"


class RubiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Rubi class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("rubi", "exclusions", "isAlways")
        data = [
                (False, "test", "a test", "tes",
                    ("a test", ("tes",), False)),
                ]
        def _checkcode(name, rubi, excls, expects):
            tmp = Rubi(name, rubi, excls)
            self.assertIsInstance(tmp, Rubi)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

