# -*- coding: utf-8 -*-
"""Test: action.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.conjuction import Then
from builder.person import Person
from builder.pronoun import Who


_FILENAME = "action.py"


class ActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Action class")

    def setUp(self):
        self.taro = Person("Taro", "山田,太郎", 15, (1,1), "male", "student")
        self.hana = Person("Hana", "田中,花子", 17, (1,1), "female", "parttimer")

    def test_attributes(self):
        attrs = ("data", "subject", "act_type", "tag_type", "note", "itemCount")
        data = [
                (False, ("test", "apple"), self.taro, ActType.ACT, TagType.NONE, "a test",
                    (("test", "apple",), self.taro, ActType.ACT, TagType.NONE, "a test", 0)),
                (False, ("test", "apple", 1), self.taro, ActType.ACT, TagType.NONE, "a test",
                    (("test", "apple",), self.taro, ActType.ACT, TagType.NONE, "a test", 1)),
                ]
        def _creator(vals, subject, act_type, tag_type, note):
            if subject and act_type and tag_type and note:
                return Action(*vals, subject=subject, act_type=act_type, tag_type=tag_type, note=note)
            elif subject and act_type and tag_type:
                return Action(*vals, subject=subject, act_type=act_type, tag_type=tag_type)
            elif subject and act_type:
                return Action(*vals, subject=subject, act_type=act_type)
            elif subject:
                return Action(*vals, subject=subject)
            else:
                return Action(*vals)
        def _checkcode(vals, subject, act_type, tag_type, note, expects):
            tmp = _creator(vals, subject, act_type, tag_type, note)
            self.assertIsInstance(tmp, Action)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_inherited(self):
        tmp = Action("apple", subject=self.taro)
        self.assertEqual(tmp.data, ("apple",))
        tmp1 = tmp.inherited("orange")
        self.assertEqual(tmp1.data, ("orange",))

    def test_conjuctionReplaced(self):
        tmp = Action("&", "apple")
        self.assertIsInstance(tmp.data[0], Then)
