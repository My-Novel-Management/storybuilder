# -*- coding: utf-8 -*-
'''
Runner class test
=================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core import reducer as rd


class ReducerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(rd.__name__, 'Reducer class')

    def test_instance(self):
        tmp = rd.Reducer()
        self.assertIsInstance(tmp, rd.Reducer)

    def test_exec_internal(self):
        data = [
                # (src, start, end, expect[chapter_num])
                (True, Story('test1',
                    Chapter('1'), Chapter('2'), Chapter('3')),
                    0, 2, 3),
                (True, Story('test2',
                    Chapter('1'), Chapter('2'), Chapter('3')),
                    1, 2, 2),
                (True, Story('test3',
                    Chapter('1'), Chapter('2'), Chapter('3')),
                    0, -1, 3),
                ]
        def checker(src, start, end, expect):
            tmp = rd.Reducer()._exec_internal(src, start, end)
            self.assertIsInstance(tmp, Story)
            self.assertEqual(len(tmp.children), expect)
        validate_with_fail(self, 'exec_internal', checker, data)
