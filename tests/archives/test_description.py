# -*- coding: utf-8 -*-
"""Test for description.py
"""
import unittest
from builder.testutils import print_test_title
from builder import description as ds
from builder import enums as em


_FILENAME = "description.py"


class DescTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Desc")

    def test_attributes(self):
        data = [
                (("test",), em.DescType.DESCRIPTION,
                    ("test",), em.DescType.DESCRIPTION),
                (("test", "apple"), em.DescType.DESCRIPTION,
                    ("test", "apple"), em.DescType.DESCRIPTION),
                ("", em.DescType.DESCRIPTION,
                    (), em.DescType.DESCRIPTION),
                (("test",), em.DescType.DIALOGUE,
                    ("test",), em.DescType.DIALOGUE),
                (("test",), em.DescType.PLAIN,
                    ("test",), em.DescType.PLAIN),
                ]

        for v, dtype, expected, exp_type in data:
            with self.subTest(v=v, dtype=dtype, expected=expected, exp_type=exp_type):
                tmp = ds.Desc(*v, desc_type=dtype)
                self.assertIsInstance(tmp, ds.Desc)
                self.assertEqual(tmp.data, expected)
                self.assertEqual(tmp.desc_type, exp_type)


class DescGroupTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "DescGroup")

    def test_attributes(self):
        dsc = ds.Desc(("test",), desc_type=em.DescType.DESCRIPTION)
        data = [
                ((dsc,), em.DescType.DESCRIPTION,
                    (dsc,), em.DescType.DESCRIPTION),
                ((dsc, dsc), em.DescType.DESCRIPTION,
                    (dsc, dsc), em.DescType.DESCRIPTION),
                ((dsc,), None,
                    (dsc,), em.DescType.DESCRIPTION),
                ]

        for v, dtype, expected, exp_type in data:
            with self.subTest(v=v, dtype=dtype, expected=expected, exp_type=exp_type):
                tmp = ds.DescGroup(base_type=dtype, *v) if dtype else ds.DescGroup(*v)
                self.assertIsInstance(tmp, ds.DescGroup)
                self.assertEqual(tmp.desc_type, exp_type)
                self.assertEqual(tmp.descriptions, expected)

