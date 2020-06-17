# -*- coding: utf-8 -*-
'''
StoryCmd class test
===================
'''

import argparse
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands import storycmd as cmd
from builder.datatypes.database import Database


class StoryCmdTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cmd.__name__, 'StoryCmd class')

    def test_instance(self):
        tmp = cmd.StoryCmd(Database())
        self.assertIsInstance(tmp, cmd.StoryCmd)

