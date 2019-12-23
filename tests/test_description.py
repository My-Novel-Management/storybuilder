# -*- coding: utf-8 -*-
"""Test: description.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder import description as ds


_FILENAME = "description.py"


class DescriptionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Description class")

    def test_attributes(self):
        data = [
                (False, ("test", "apple"), ds.DescType.DESC,
                    ("test", "apple"), ds.DescType.DESC,),
                (False, ("test",), ds.DescType.DESC,
                    ("test",), ds.DescType.DESC,),
                (False, ("test", "apple"), ds.DescType.DIALOGUE,
                    ("test", "apple"), ds.DescType.DIALOGUE,),
                (False, ("test", "apple"), ds.DescType.COMPLEX,
                    ("test", "apple"), ds.DescType.COMPLEX,),
                (False, ("test", "apple"), None,
                    ("test", "apple"), ds.DescType.DESC,),
                (True, (1,2), ds.DescType.DESC,
                    (1,2), ds.DescType.DESC,),
                ]
        def _checkcode(vals, dtype, expect, exp_type):
            tmp = ds.Description(*vals, desc_type=dtype) if dtype else ds.Description(*vals)
            self.assertIsInstance(tmp, ds.Description)
            self.assertEqual(tmp.descs, expect)
            self.assertEqual(tmp.desc_type, exp_type)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_attr_descs_when_single_string(self):
        tmp = ds.Description("testing")
        self.assertEqual(tmp.descs, ("testing",))

class NoDescTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "NoDesc class")

    def test_attributes(self):
        tmp = ds.NoDesc()
        self.assertIsInstance(tmp, ds.NoDesc)

class RubiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Rubi class")

    def test_attributes(self):
        data = [
                (False, ("test", "apple"), ds.RubiType.EVERY,
                    "test", "apple", ds.RubiType.EVERY),
                ]
        def _checkcode(vals, t, exp_base, exp_rubi, exp_type):
            tmp = ds.Rubi(*vals, rubi_type=t) if t else ds.Rubi(*vals)
            self.assertIsInstance(tmp, ds.Rubi)
            self.assertEqual(tmp.base, exp_base)
            self.assertEqual(tmp.rubi, exp_rubi)
            self.assertEqual(tmp.rubi_type, exp_type)
