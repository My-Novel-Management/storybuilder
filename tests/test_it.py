# -*- coding: utf-8 -*-
"""Test: it.py
"""
import unittest
from testutils import print_test_title
from builder import it


_FILENAME = "it.py"


class ItTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "It class")

    def test_attributes(self):
        tmp = it.It()
        self.assertIsInstance(tmp, it.It)
        self.assertEqual(tmp.name, it.It.__NAME__)
