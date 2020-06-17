# -*- coding: utf-8 -*-
'''
OutputMode Enum class test
==========================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import outputmode as om


class OutputModeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(om.__name__, 'OutputMode Enum class')

    def test_instance(self):
        self.assertEqual(
                len(om.OutputMode.get_all()),
                2)

