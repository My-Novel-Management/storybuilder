# -*- coding: utf-8 -*-
'''
Runner class test
=================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.core import runner as rn


class RunnerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(rn.__name__, 'Runner class')

    def test_instance(self):
        tmp = rn.Runner()
        self.assertIsInstance(tmp, rn.Runner)

