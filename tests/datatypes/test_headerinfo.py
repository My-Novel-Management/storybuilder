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
                # (chars, t_lines, t_papers, lines, papers, chaps, epis, scenes, scodes,
                #   exp_chars, exp_tlines, exp_tpapers, exp_lines, exp_papers, exp_chaps, exp_epis, exp_scenes, exp_scodes)
                (True, 9, 9, 9, 1, 10, 100, 5, 5, 5, 5,
                    9, 9, 9, 1, 10, 100, 5,5,5,5),
                ]
        def checker(total, t_lines, t_papers, chars, lines, papers, chapters, episodes, scenes, scodes,
                exp_total, exp_tlines, exp_tpapers, exp_chars, exp_lines, exp_papers, exp_chaps, exp_epis, exp_scenes, exp_scodes):
            tmp = hd.HeaderInfo(total, t_lines, t_papers, chars, lines, papers, chapters, episodes, scenes, scodes)
            self.assertIsInstance(tmp, hd.HeaderInfo)
            self.assertEqual(tmp.total_chars, exp_total)
            self.assertEqual(tmp.total_lines, exp_tlines)
            self.assertEqual(tmp.total_papers, exp_tpapers)
            self.assertEqual(tmp.desc_chars, exp_chars)
            self.assertEqual(tmp.lines, exp_lines)
            self.assertEqual(tmp.papers, exp_papers)
            self.assertEqual(tmp.chapters, exp_chaps)
            self.assertEqual(tmp.episodes, exp_epis)
            self.assertEqual(tmp.scenes, exp_scenes)
            self.assertEqual(tmp.scodes, exp_scodes)
        validate_with_fail(self, 'class instance', checker, data)
