# -*- coding: utf-8 -*-
"""Test: layer.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.layer import Layer


_FILENAME = "layer.py"


class LayerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Layer class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("words",)
        data = [
                (False, "test", "a test",
                    (("a test",),)),
                ]
        def _checkcode(name, words, expects):
            tmp = Layer(name, words)
            self.assertIsInstance(tmp, Layer)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

