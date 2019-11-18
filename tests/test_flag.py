# -*- coding: utf-8 -*-
"""Test: flag.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.flag import Flag, NoDeflag, NoFlag


_FILENAME = "flag.py"


class FlagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Flag class")

    def test_attributes(self):
        data = [
                (False, "test", False,),
                (False, "test", True,),
                (True, 1, False,),
                ]
        def _checkcode(info, isdeflag):
            tmp = Flag(info, isdeflag)
            self.assertIsInstance(tmp, Flag)
            self.assertEqual(tmp.info, info)
            self.assertEqual(tmp.isDeflag, isdeflag)
        validated_testing_withfail(self, "attributes", _checkcode, data)

class NoFlagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "NoFlag class")

    def test_attributes(self):
        tmp = NoFlag()
        self.assertIsInstance(tmp, NoFlag)
        self.assertEqual(tmp.info, NoFlag.__NAME__)
        self.assertEqual(tmp.isDeflag, False)

class NoDeflagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "NoDeflag class")

    def test_attributes(self):
        tmp = NoDeflag()
        self.assertIsInstance(tmp, NoDeflag)
        self.assertEqual(tmp.info, NoDeflag.__NAME__)
        self.assertEqual(tmp.isDeflag, True)
