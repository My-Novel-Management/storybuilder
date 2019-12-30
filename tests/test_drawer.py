# -*- coding: utf-8 -*-
"""Test: drawer.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local file_
from builder.drawer import Drawer
from builder.shot import Shot


_FILENAME = "drawer.py"


class DrawerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Drawer class")

    def setUp(self):
        pass

    def test_attributes(self):
        data = [
                (False, None,),
                ]
        def _checkcode(v):
            tmp = Drawer(v)
            self.assertIsInstance(tmp, Drawer)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

