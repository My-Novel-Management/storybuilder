# -*- coding: utf-8 -*-
"""Test: baseactor.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local file_
from builder.baseactor import BaseActor
from builder.basedata import BaseData
from tests import __BASE_ID__


_FILENAME = "baseactor.py"


class BaseActorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "BaseActor class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("src", "actId")
        bd1 = BaseData("test", ())
        data = [
                (False, bd1,
                    (bd1, __BASE_ID__ + 42)),
                ]
        def _checkcode(src, expects):
            tmp = BaseActor(src)
            self.assertIsInstance(tmp, BaseActor)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

