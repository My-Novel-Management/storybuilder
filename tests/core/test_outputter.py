# -*- coding: utf-8 -*-
'''
Outputter class test
====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.core import outputter as ot


class OutputterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(ot.__name__, 'Outputter class')

    def test_instance(self):
        tmp = ot.Outputter()
        self.assertIsInstance(tmp, ot.Outputter)

