# -*- coding: utf-8 -*-
"""Test: combaction.py
"""
import unittest
from testutils import print_test_title
from builder import combaction as ca
from builder.action import Action
from builder.person import Person


_FILENAME = "combaction.py"


class CombActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "CombAction class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")

    def test_attributes(self):
        act1 = Action(self.taro, "")
        data = [
                ((act1,), False),
                ([1,2,3], True),
                ]
        for acts, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = ca.CombAction(*acts)
                    self.assertIsInstance(tmp, ca.CombAction)
                    self.assertEqual(tmp.title, ca.CombAction.__NAME__)
                    self.assertEqual(tmp.actions, acts)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = ca.CombAction(*acts)
                        self.assertIsInstance(tmp, ca.CombAction)
                        self.assertEqual(tmp.title, ca.CombAction.__NAME__)
                        self.assertEqual(tmp.actions, acts)

    def test_inherited(self):
        act1 = Action(self.taro, "test")
        data = [
                ((act1,), False),
                ([1,2,3], True),
                ]
        for acts, isfail in data:
            with self.subTest():
                tmp = ca.CombAction()
                if not isfail:
                    tmp1 = tmp.inherited(*acts)
                    self.assertIsInstance(tmp1, ca.CombAction)
                    self.assertEqual(tmp1.actions, acts)
                else:
                    with self.assertRaises(AssertionError):
                        tmp1 = tmp.inherited(*acts)
                        self.assertIsInstance(tmp1, ca.CombAction)
                        self.assertEqual(tmp1.actions, acts)
