# -*- coding: utf-8 -*-
"""Test: chara.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import chara as ch


_FILENAME = "chara.py"


class CharaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Chara class")

    def test_attributes(self):
        data = [
                (False, "test",),
                (True, 1,),
                ]
        def _checkcode(name):
            tmp = ch.Chara(name)
            self.assertIsInstance(tmp, ch.Chara)
            self.assertEqual(tmp.name, name)
        validated_testing_withfail(self, "attributes", _checkcode, data)

