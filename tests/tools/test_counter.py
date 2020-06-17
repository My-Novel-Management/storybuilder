# -*- coding: utf-8 -*-
'''
Counter class test
==================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.tools import counter as cnt


class CounterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cnt.__name__, 'Counter class')

    def test_chapters_of(self):
        data = [
                # (src, expect[int])
                (True, Story('a', Chapter('b',)), 1),
                (True, Chapter('a',), 1),
                (True, Episode('a',), 0),
                (True, Scene('a',), 0),
                (True, SCode(None, SCmd.BE, (),""), 0),
                ]
        validate_with_fail(self, 'chapters_of',
                lambda src, expect: self.assertEqual(
                    cnt.Counter().chapters_of(src), expect),
                data)

    def test_episodes_of(self):
        data = [
                # (src, expect[int])
                (True, Story('a', Chapter('b', Episode('c',))), 1),
                (True, Chapter('a', Episode('b',)), 1),
                (True, Episode('a',), 1),
                (True, Scene('a',), 0),
                (True, SCode(None, SCmd.BE, (),''), 0),
                ]
        validate_with_fail(self, 'episodes_of',
                lambda src, expect: self.assertEqual(
                    cnt.Counter().episodes_of(src), expect),
                data)

    def test_scenes_of(self):
        data = [
                # (src, expect[int])
                (True, Story('a', Chapter('b', Episode('c', Scene('d',)))), 1),
                (True, Chapter('a', Episode('b', Scene('c',))), 1),
                (True, Episode('a', Scene('b',)), 1),
                (True, Scene('a',), 1),
                (True, SCode(None, SCmd.BE, (), ''), 0),
                ]
        validate_with_fail(self, 'scenes_of',
                lambda src, expect: self.assertEqual(
                    cnt.Counter().scenes_of(src), expect),
                data)

    def test_scodes_of(self):
        data = [
                # (src, expect[int])
                (True, Story('a', Chapter('b', Episode('c', Scene('d',
                    SCode(None, SCmd.BE, (),''))))), 1),
                (True, Chapter('a', Episode('b', Scene('c',
                    SCode(None, SCmd.BE, (),'')))), 1),
                (True, Episode('a', Scene('b', SCode(None, SCmd.BE, (),''))), 1),
                (True, Scene('a', SCode(None, SCmd.BE, (),'')), 1),
                (True, SCode(None, SCmd.BE, (),''), 1),
                ]
        validate_with_fail(self, 'scodes_of',
                lambda src, expect: self.assertEqual(
                    cnt.Counter().scodes_of(src), expect),
                data)

    def test_scodes_of_without_info(self):
        scode0 = SCode(None, SCmd.BE, (), '')
        sinfo = SCode(None, SCmd.INFO_DATA, (),'')
        data = [
                # (src, expect[int])
                (True, Story('a', Chapter('b', Episode('c', Scene('d',
                    scode0, sinfo)))), 1),
                (True, Chapter('a', Episode('b', Scene('c',
                    scode0, sinfo))), 1),
                (True, Episode('a', Scene('b', scode0, sinfo)), 1),
                (True, Scene('a', scode0, sinfo), 1),
                (True, scode0, 1),
                (True, sinfo, 0),
                ]
        validate_with_fail(self, 'scode_of_without_info',
                lambda src, expect: self.assertEqual(
                    cnt.Counter().scodes_of_without_info(src), expect),
                data)

    def test_description_characters_of(self):
        scode0 = SCode(None, SCmd.BE, ('apple',), '')
        scode1 = SCode(None, SCmd.DO, ('orange',), '')
        sinfo = SCode(None, SCmd.INFO_DATA, ('test',), '')
        data = [
                # (src, expect[int])
                (True, Story('a', Chapter('b', Episode('c', Scene('d',
                    scode0, scode1, sinfo)))), 13),
                (True, Chapter('a', Episode('b', Scene('c',
                    scode0, scode1, sinfo))), 13),
                (True, Episode('a', Scene('b', scode0, scode1, sinfo)), 13),
                (True, Scene('a', scode0, scode1, sinfo), 13),
                (True, scode0, 6),
                (True, sinfo, 0),
                (True, [scode0, scode1], 13),
                ]
        validate_with_fail(self, 'description_characters_of',
                lambda src, expect: self.assertEqual(
                    cnt.Counter().description_characters_of(src), expect),
                data)

    def test_manupaper_numbers_of(self):
        data = [
                # (lines, rows, expect[float])
                (True, 40, 20, 2),
                (True, 50, 20, 2.5),
                (True, 50, 0, 0),
                ]
        validate_with_fail(self, 'manupaper_numbers_of',
                lambda lines, rows, expect: self.assertEqual(
                    cnt.Counter().manupaper_numbers_of(lines, rows), expect),
                data)

    def test_manupaper_rows_of(self):
        scode0 = SCode(None, SCmd.BE, ('apple',), '')
        scode1 = SCode(None, SCmd.DO, ('orange',), '')
        scode2 = SCode(None, SCmd.TALK, ('melon',), '')
        data = [
                # (src, columns, expect[int])
                (True, Story('a', Chapter('b', Episode('c', Scene('d',
                    scode0, scode1, scode2)))), 20, 3),
                (True, Chapter('a', Episode('b', Scene('c',
                    scode0, scode1, scode2))), 20, 3),
                (True, Episode('a', Scene('b',
                    scode0, scode1, scode2)), 20, 3),
                (True, Scene('a',
                    scode0, scode1, scode2), 20, 3),
                (True, scode0, 20, 1),
                (True, [scode0, scode1, scode2], 20, 3),
                (True, SCode(None, SCmd.DO, ('a'*10,)), 5, 3),
                ]
        validate_with_fail(self, 'manupaper_rows_of',
                lambda src, columns, expect: self.assertEqual(
                    cnt.Counter().manupaper_rows_of(src, columns), expect),
                data)
