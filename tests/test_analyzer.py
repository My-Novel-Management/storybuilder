# -*- coding: utf-8 -*-
"""Test: analyzer.py
"""
import unittest
from testutils import print_test_title
from builder.analyzer import Analyzer


_FILENAME = "analyzer.py"


class AnalyzerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Analyzer class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = Analyzer("")
