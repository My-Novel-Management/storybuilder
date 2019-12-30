# -*- coding: utf-8 -*-
"""Test: parser.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.action import Action
from builder.datapack import DataPack
from builder.parser import Parser
from builder.person import Person
from builder.rubi import Rubi
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


_FILENAME = "parser.py"


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Parser class")

    def setUp(self):
        self.taro = Person("Taro", "", 15, "male", "student", "me:俺")

    def test_attributes(self):
        tmp = Parser(Story("test"))
        self.assertIsInstance(tmp, Parser)

    def test_toDescriptionsWithRubi(self):
        data = [
                (False, Scene("sc", Action("a", Shot("山本"))),
                    {"山":Rubi("山","山《やま》", "")},
                    DataPack("desc", "山《やま》本。")),
                ]
        def _checkcode(v, rubis, expect):
            tmp = Parser(v).toDescriptionsWithRubi(rubis)
            self.assertEqual(tmp[1], expect)
        validatedTestingWithFail(self, "toDescriptionsWithRubi", _checkcode, data)
