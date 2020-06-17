# -*- coding: utf-8 -*-
'''
TagReplacer class test
======================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.objects.person import Person
from builder.core import tagreplacer as tp


class TagReplacerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(tp.__name__, 'TagReplacer class')

    def setUp(self):
        self.taro = Person('太郎', '', 17,(1,1), 'male', 'student',
                'me:俺')

    def test_instance(self):
        tmp = tp.TagReplacer()
        self.assertIsInstance(tmp, tp.TagReplacer)

    def test_replaced_scode(self):
        data = [
                # src, tags, expect
                (True, SCode(None, SCmd.DO, ('$taroは話した',),),
                    {'taro': '太郎'},
                    ('太郎は話した',),),
                (True, SCode(self.taro, SCmd.DO, ('$meは話した', '$herは逃げた'),),
                    {'her': '華子'},
                    ('俺は話した','華子は逃げた'),),
                ]
        validate_with_fail(self, 'replaced_scode',
                lambda src, tags, expect: self.assertEqual(
                    tp.TagReplacer()._replaced_scode(src, tags).script, expect),
                data)
