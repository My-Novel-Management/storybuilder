# -*- coding: utf-8 -*-
"""Test: formatter.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import __FORMAT_DEFAULT__
from builder import DataType, ConteData
from builder import ActType
from builder.analyzer import Analyzer
from builder.formatter import Formatter



_FILENAME = "formatter.py"


class FormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Formatter class")

    def setUp(self):
        self.anal = Analyzer("")

    def test_attributes(self):
        tmp = Formatter()
        self.assertIsInstance(tmp, Formatter)

    def test_toConte(self):
        data = [
                (False, ((DataType.SCENE_TITLE, "apple"),
                    (DataType.ACTION,
                        ConteData(ActType.TALK, "Im", "太郎", [], "テスト", 0, "a note"))),
                    ["# test\n", "\n** Sc-1: apple **\n",
                        "TA|Im"+"　"*22 + "|太郎"+"　"*30+"|テスト"+"　"*21+"|a note"]),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Formatter.toConte("test", v, self.anal), expect)
        validatedTestingWithFail(self, "toConte", _checkcode, data)

    def test_toDescription(self):
        data = [
                (False, ((DataType.SCENE_TITLE, "apple"), (DataType.DESCRIPTION, "orange")),
                    ["# test\n", "\n** Sc-1: apple **\n", "　orange"]),
                (False, ((DataType.SCENE_TITLE, "apple"), (DataType.DIALOGUE, "orange")),
                    ["# test\n", "\n** Sc-1: apple **\n", "「orange」"]),
                (False, ((DataType.SCENE_TITLE, "apple"), (DataType.VOICE, "orange")),
                    ["# test\n", "\n** Sc-1: apple **\n", "『orange』"]),
                ]
        def _checkcode(v, expect):
            self.assertEqual(Formatter.toDescription("test", v, __FORMAT_DEFAULT__), expect)
        validatedTestingWithFail(self, "toDescription", _checkcode, data)
