# -*- coding: utf-8 -*-
"""Test for basesubject.py
"""
import unittest
from builder.testutils import print_test_title
from builder import baseaction as ba
from builder import enums as em

_FILENAME = "baseaction.py"


class BaseActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "BaseAction")

    def test_attributes(self):
        data = [
                (em.ActType.BE, em.ActType.BE),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = ba.BaseAction(v)
                self.assertIsInstance(tmp, ba.BaseAction)
                self.assertEqual(tmp.act_type, expected)

