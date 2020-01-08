# -*- coding: utf-8 -*-
"""Test: writer.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.person import Person
from builder.writer import Writer


_FILENAME = "writer.py"


class WriterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Writer class")

    def setUp(self):
        self.taro = Person("Taro", "", 15, (1,1), "male", "student")

    def test_attributes(self):
        tmp = Writer(self.taro)
        self.assertIsInstance(tmp, Writer)

