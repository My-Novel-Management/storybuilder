# -*- coding: utf-8 -*-
'''
Serializer class test
=====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.datatypes.compilemode import CompileMode
from builder.core import serializer as sl


class SerializerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(sl.__name__, 'Serializer class')

    def test_instance(self):
        tmp = sl.Serializer()
        self.assertIsInstance(tmp, sl.Serializer)

    def test_novel_serialized(self):
        scode0 = SCode(None, SCmd.BE, (), '')
        scode1 = SCode(None, SCmd.INFO_DATA, (), '')
        data = [
                # (src, expect)
                (True, Chapter('a', Episode('b', Scene('c', scode0))),
                    1),
                (True, Chapter('a', scode1, Episode('b', Scene('c', scode0))),
                    2),
                ]
        validate_with_fail(self, 'novel_serialized',
                lambda src, expect: self.assertEqual(
                    len(sl.Serializer()._novel_serialized(src)), expect),
                data)
