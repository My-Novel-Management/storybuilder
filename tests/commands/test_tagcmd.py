# -*- coding: utf-8 -*-
'''
TagCmd class test
=================
'''

import argparse
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands import tagcmd as cmd


class TagCmdTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cmd.__name__, 'TagCmd class')

    def test_instance(self):
        tmp = cmd.TagCmd()
        self.assertIsInstance(tmp, cmd.TagCmd)

