# -*- coding: utf-8 -*-
"""Test: action.py
"""
import unittest
from testutils import print_test_title
from builder import action as ac


_FILENAME = "action.py"


class ActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Action class")

    def test_attributes(self):
        a = ac.Action(None, "test outline", ac.ActType.LOOK)
        self.assertIsInstance(a, ac.Action)
        self.assertIsInstance(a.subject, ac.NoSubject)
        self.assertEqual(a.outline, "test outline")
        self.assertIsInstance(a.getFlag(), ac.NoFlag)
        self.assertIsInstance(a.getDeflag(), ac.NoDeflag)
        self.assertIsInstance(a.description, ac.NoDesc)

    def test_method_desc(self):
        a = ac.Action("", "test outline", ac.ActType.ACT)
        a.desc("test", "apple")
        self.assertNotIsInstance(a.description, ac.NoDesc)
        self.assertEqual(a.description.descs, ("test", "apple"))
