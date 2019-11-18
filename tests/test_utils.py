# -*- coding: utf-8 -*-
"""Test: utils.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import utils as utl
from builder.action import Action
from builder.description import Description
from builder.person import Person


_FILENAME = "utils.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "utils methods")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")

    def test_strOfDescription(self):
        data = [
                (False, Action(self.taro, "a test").d("彼は", "太郎だ"),
                    "彼は太郎だ",),
                (False, Action(self.taro, "a test").d("彼は太郎だ"),
                    "彼は太郎だ",),
                (True, [1,2,3],
                    "彼は太郎だ",),
                ]
        def _checkcode(act, expect):
            tmp = utl.strOfDescription(act)
            self.assertIsInstance(tmp, str)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "strOfDescription", _checkcode, data)
