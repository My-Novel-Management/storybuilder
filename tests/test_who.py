# -*- coding: utf-8 -*-
"""Test: who.py
"""
import unittest
from testutils import print_test_title
from builder.who import Who, When, Where


_FILENAME = "who.py"


class WhoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Who class")

    def test_attributes(self):
        tmp = Who()
        self.assertIsInstance(tmp, Who)
        self.assertEqual(tmp.name, Who.__NAME__)

class WhenTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "When class")

    def test_attributes(self):
        tmp = When()
        self.assertIsInstance(tmp, When)
        self.assertEqual(tmp.name, When.__NAME__)

class WhereTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Where class")

    def test_attributes(self):
        tmp = Where()
        self.assertIsInstance(tmp, Where)
        self.assertEqual(tmp.name, Where.__NAME__)

