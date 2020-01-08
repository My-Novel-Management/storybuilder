# -*- coding: utf-8 -*-
"""Test: lifenote.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.action import Action
from builder.lifenote import LifeNote
from builder.person import Person


_FILENAME = "lifenote.py"


class LifeNoteTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "LifeNote class")

    def setUp(self):
        self.taro = Person("Taro", "", 15, (1,1), "male", "student")

    def test_attributes(self):
        attrs = ("data", "subject")
        act1 = Action("apple")
        act2 = Action("orange")
        data = [
                (False, "test", self.taro, (act1, act2),
                    ((act1, act2), self.taro)),
                ]
        def _checkcode(title, subject, vals, expects):
            tmp = LifeNote(title, subject, *vals)
            self.assertIsInstance(tmp, LifeNote)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    def test_inherited(self):
        ac1, ac2 = Action("apple"), Action("orange")
        tmp = LifeNote("test", self.taro, ac1)
        self.assertEqual(tmp.data, (ac1,))
        tmp1 = tmp.inherited(ac2)
        self.assertEqual(tmp1.data, (ac2,))
