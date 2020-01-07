# -*- coding: utf-8 -*-
"""Test: metadata.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import MetaType
from builder.metadata import MetaData


_FILENAME = "metadata.py"


class MetaDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "MetaData class")

    def setUp(self):
        pass

    def test_attributes(self):
        tmp = MetaData(info="test")
        self.assertIsInstance(tmp, MetaData)
        self.assertEqual(tmp.note, "test")

