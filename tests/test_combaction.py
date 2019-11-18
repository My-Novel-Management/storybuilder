# -*- coding: utf-8 -*-
"""Test: combaction.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
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
                (False, (act1,),),
                (True, [1,2,3],),
                ]
        def _checkcode(acts):
            tmp = ca.CombAction(*acts)
            self.assertIsInstance(tmp, ca.CombAction)
            self.assertEqual(tmp.title, ca.CombAction.__NAME__)
            self.assertEqual(tmp.actions, acts)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        act1 = Action(self.taro, "test")
        data = [
                (False, (act1,),),
                (True, [1,2,3],),
                ]
        def _checkcode(acts):
            tmp = ca.CombAction()
            tmp1 = tmp.inherited(*acts)
            self.assertIsInstance(tmp1, ca.CombAction)
            self.assertEqual(tmp1.actions, acts)
        validated_testing_withfail(self, "inherited", _checkcode, data)
