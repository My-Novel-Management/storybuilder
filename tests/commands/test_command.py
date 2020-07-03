# -*- coding: utf-8 -*-
'''
Command enum test
=================
'''

import argparse
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands import command as cmd


class SCmdEnumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cmd.__name__, 'SCmd enum class')

    def test_get_commandline_arguments(self):
        self.assertEqual(
                set(cmd.SCmd.get_all_actions()),
                set(cmd.SCmd.get_normal_actions() + cmd.SCmd.get_dialogue_actions()))
        self.assertEqual(
                set(cmd.SCmd.get_all()),
                set(
                    cmd.SCmd.get_all_actions() \
                    + cmd.SCmd.get_end_of_containers() \
                    + cmd.SCmd.get_head_of_containers() \
                    + cmd.SCmd.get_informations() \
                    + cmd.SCmd.get_scene_controls() \
                    + cmd.SCmd.get_plot_infos() \
                    + cmd.SCmd.get_tags() \
                    + [cmd.SCmd.THEN]
                    )
                )
