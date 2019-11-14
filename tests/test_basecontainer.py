# -*- coding: utf-8 -*-
"""Test: basecontainer.py
"""
import unittest
from testutils import print_test_title
from builder import basecontainer as bs


_FILENAME = "basecontainer.py"


class BaseContainerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseContainer class")

    def test_attributes(self):
        data = [
                ]
        for title, pri in data:
            with self.subTest():
                tmp = bs.BaseContainer(title, pri)
                self.assertIsInstance(tmp, bs.BaseContainer)
                self.assertEqual(tmp.title, title)
                self.assertEqual(tmp.priority, pri)

    def test_setPriority(self):
        data = [
                (5, 5, False),
                (20, 20, True),
                ]
        for v, expect, isfail in data:
            with self.subTest():
                tmp = bs.BaseContainer("test", 1)
                if not isfail:
                    self.assertIsInstance(tmp.setPriority(v), bs.BaseContainer)
                    self.assertEqual(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        self.assertIsInstance(tmp.setPriority(v), bs.BaseContainer)
