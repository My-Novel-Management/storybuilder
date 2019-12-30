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
from builder.person import Person
from builder.who import Who


_FILENAME = "action.py"


class ActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Action class")

    def setUp(self):
        self.taro = Person("Taro", "山田,太郎", 15, "male", "student")

    def test_attributes(self):
        attrs = ("acts", "doing", "subject", "act_type", "tag_type", "note",)
        data = [
                (False, ("test", "apple"), self.taro, ActType.ACT, TagType.NONE, "a test",
                    (("apple",), "test", self.taro, ActType.ACT, TagType.NONE, "a test")),
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

