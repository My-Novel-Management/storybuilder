# -*- coding: utf-8 -*-
"""Test: flag.py
"""
import unittest
from testutils import print_test_title
from builder.flag import Flag, NoDeflag, NoFlag


_FILENAME = "flag.py"


class FlagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Flag class")

    def test_attributes(self):
        data = [
                ("test", False, False),
                ("test", True, False),
                (1, False, True),
                ]
        for info, isdeflag, isfail in data:
            with self.subTest():
                if not isfail:
                    tmp = Flag(info, isdeflag)
                    self.assertIsInstance(tmp, Flag)
                    self.assertEqual(tmp.info, info)
                    self.assertEqual(tmp.isDeflag, isdeflag)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = Flag(info, isdeflag)
                        self.assertIsInstance(tmp, Flag)
                        self.assertEqual(tmp.info, info)
                        self.assertEqual(tmp.isDeflag, isdeflag)

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
