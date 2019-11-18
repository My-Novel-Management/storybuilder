# -*- coding: utf-8 -*-
"""Test: basecontainer.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import basecontainer as bs


_FILENAME = "basecontainer.py"


class BaseContainerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseContainer class")

    def test_attributes(self):
        data = [
                (False, "test", 1,),
                ]
        def _checkcode(title, pri):
            tmp = bs.BaseContainer(title, pri)
            self.assertIsInstance(tmp, bs.BaseContainer)
            self.assertEqual(tmp.title, title)
            self.assertEqual(tmp.priority, pri)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_setPriority(self):
        data = [
                (False, 5, 5,),
                (True, 20, 20,),
                ]
        def _checkcode(v, expect):
            tmp = bs.BaseContainer("test", 1)
            self.assertIsInstance(tmp.setPriority(v), bs.BaseContainer)
            self.assertEqual(v, expect)
        validated_testing_withfail(self, "setPriority", _checkcode, data)
