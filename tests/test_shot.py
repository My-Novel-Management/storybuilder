# -*- coding: utf-8 -*-
"""Test: shot.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.shot import Shot


_FILENAME = "shot.py"


class ShotTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Shot class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("infos", "isTerm")
        data = [
                (False, "a test",
                    (("a test",), False)),
                ]
        def _checkcode(info, expects):
            tmp = Shot(info)
            self.assertIsInstance(tmp, Shot)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

