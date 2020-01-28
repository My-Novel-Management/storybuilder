# -*- coding: utf-8 -*-
"""Test: basedata.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.basedata import BaseData


_FILENAME = "basedata.py"


class BaseDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "BaseData class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("name", "data", "note", "texture")
        data = [
                (False, "test", "a", "a note",
                    ("test", "a", "a note", "")),
                ]
        def _checkcode(name, data, note, expects):
            tmp = BaseData(name, *data, note=note)
            self.assertIsInstance(tmp, BaseData)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_dataId(self):
        tmp = BaseData("test")
        self.assertIsInstance(tmp.dataId, int)

    def test_texture(self):
        tmp = BaseData("test")
        self.assertEqual(tmp.texture, "")
        tmp.setTexture("apple")
        self.assertEqual(tmp.texture, "apple")
