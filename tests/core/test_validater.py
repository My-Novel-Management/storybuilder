# -*- coding: utf-8 -*-
'''
Validater class test
====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.core import validater as vd


class ValidaterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(vd.__name__, 'Validater class')

    def test_instance(self):
        tmp = vd.Validater()
        self.assertIsInstance(tmp, vd.Validater)

