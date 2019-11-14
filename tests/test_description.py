# -*- coding: utf-8 -*-
"""Test: description.py
"""
import unittest
from testutils import print_test_title
from builder import description as ds


_FILENAME = "description.py"


class DescriptionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Description class")

    def test_attributes(self):
        data = [
                (("test", "apple"), ds.DescType.DESC,
                    ("test", "apple"), ds.DescType.DESC, False),
                (("test",), ds.DescType.DESC,
                    ("test",), ds.DescType.DESC, False),
                (("test", "apple"), ds.DescType.DIALOGUE,
                    ("test", "apple"), ds.DescType.DIALOGUE, False),
                (("test", "apple"), ds.DescType.COMPLEX,
                    ("test", "apple"), ds.DescType.COMPLEX, False),
                (("test", "apple"), None,
                    ("test", "apple"), ds.DescType.DESC, False),
                ((1,2), ds.DescType.DESC,
                    (1,2), ds.DescType.DESC, True),
                ]
        for vals, dtype, expect, exp_type, isfail in data:
            with self.subTest(vals=vals):
                if not isfail:
                    tmp = ds.Description(*vals, desc_type=dtype) if dtype else ds.Description(*vals)
                    self.assertIsInstance(tmp, ds.Description)
                    self.assertEqual(tmp.descs, expect)
                    self.assertEqual(tmp.desc_type, exp_type)
                else:
                    with self.assertRaises(AssertionError):
                        tmp = ds.Description(*vals, desc_type=dtype) if dtype else ds.Description(*vals)
                        self.assertIsInstance(tmp, ds.Description)
                        self.assertEqual(tmp.descs, expect)
                        self.assertEqual(tmp.desc_type, exp_type)

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
