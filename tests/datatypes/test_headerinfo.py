# -*- coding: utf-8 -*-
'''
HeaderInfo class test
=====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import headerinfo as hd


class HeaderInfoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(hd.__name__, 'HeaderInfo class')

    def test_instance(self):
        data = [
                # (chars, lines, papers, chaps, epis, scenes, scodes,
                #   exp_chars, exp_lines, exp_papers, exp_chaps, exp_epis, exp_scenes, exp_scodes)
                (True, 1, 10, 100, 5, 5, 5, 5,
                    1, 10, 100, 5,5,5,5),
                ]
        def checker(chars, lines, papers, chapters, episodes, scenes, scodes,
                exp_chars, exp_lines, exp_papers, exp_chaps, exp_epis, exp_scenes, exp_scodes):
            tmp = hd.HeaderInfo(chars, lines, papers, chapters, episodes, scenes, scodes)
            self.assertIsInstance(tmp, hd.HeaderInfo)
            self.assertEqual(tmp.desc_chars, exp_chars)
            self.assertEqual(tmp.lines, exp_lines)
            self.assertEqual(tmp.papers, exp_papers)
            self.assertEqual(tmp.chapters, exp_chaps)
            self.assertEqual(tmp.episodes, exp_epis)
            self.assertEqual(tmp.scenes, exp_scenes)
            self.assertEqual(tmp.scodes, exp_scodes)
        validate_with_fail(self, 'class instance', checker, data)
