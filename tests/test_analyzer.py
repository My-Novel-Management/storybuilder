# -*- coding: utf-8 -*-
"""Test: analyzer.py
"""
## public libs
import unittest
## third libs
import MeCab
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.analyzer import Analyzer


_FILENAME = "analyzer.py"


class AnalyzerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Analyzer class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = Analyzer("")
        self.assertIsInstance(tmp, Analyzer)
