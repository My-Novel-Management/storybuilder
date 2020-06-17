# -*- coding: utf-8 -*-
'''
HeaderUpdater class test
========================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core import headerupdater as hd


class HeaderUpdaterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(hd.__name__, 'HeaderUpdater class')

    def test_instance(self):
        tmp = hd.HeaderUpdater()
        self.assertIsInstance(tmp, hd.HeaderUpdater)

    def test_title_of(self):
        data = [
                # (src, expect, exp_opt)
                (True, Story('test',), ('test',), 1),
                ]
        def checker(src, expect, exp_opt):
            tmp = hd.HeaderUpdater()._title_of(src)
            self.assertIsInstance(tmp, SCode)
            self.assertEqual(tmp.cmd, SCmd.TAG_TITLE)
            self.assertEqual(tmp.script, expect)
            self.assertEqual(tmp.option, exp_opt)
        validate_with_fail(self, 'title_of', checker, data)

    def test_outline_of(self):
        data = [
                # (src, expect)
                (True, Story('test',outline='apple'), ('apple',)),
                ]
        def checker(src, expect):
            tmp = hd.HeaderUpdater()._outline_of(src)
            self.assertIsInstance(tmp, SCode)
            self.assertEqual(tmp.cmd, SCmd.TAG_COMMENT)
            self.assertEqual(tmp.script, expect)
        validate_with_fail(self, 'outline_of', checker, data)

    def test_end_of(self):
        data = [
                # (src, expect)
                (True, Chapter('test',), SCmd.END_CHAPTER),
                ]
        validate_with_fail(self, 'end_of',
                lambda src, expect: self.assertEqual(
                    hd.HeaderUpdater()._end_of(src).cmd, expect),
                data)
