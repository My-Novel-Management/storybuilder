# -*- coding: utf-8 -*-
"""Test: block.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.action import Action
from builder.block import Block


_FILENAME = "block.py"


class BlockTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Block class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("data",)
        act1 = Action("apple")
        act2 = Action("orange")
        data = [
                (False, "test", (act1, act2),
                    ((act1, act2),)),
                ]
        def _checkcode(title, vals, expects):
            tmp = Block(title, *vals)
            self.assertIsInstance(tmp, Block)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_inherited(self):
        ac1, ac2 = Action("apple"), Action("orange")
        tmp = Block("test", ac1)
        self.assertEqual(tmp.data, (ac1,))
        tmp1 = tmp.inherited(ac2)
        self.assertEqual(tmp1.data, (ac2,))
