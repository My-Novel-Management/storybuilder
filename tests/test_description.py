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
        d = ds.Description("test1", "test2", desc_type=ds.DescType.DESC)
        self.assertIsInstance(d, ds.Description)
        self.assertEqual(d.descs, ("test1", "test2"))
        self.assertEqual(d.desc_type, ds.DescType.DESC)

