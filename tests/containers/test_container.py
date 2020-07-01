# -*- coding: utf-8 -*-
'''
Container class test
====================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.containers import container as cnt
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.material import Material, MaterialType
from builder.containers.scene import Scene
from builder.containers.story import Story


class ContainerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cnt.__name__, 'Container class')

    def test_instance(self):
        data = [
                # (title, args, outline, exp_title, exp_args, exp_outline)
                (True, 'test', ('apple','orange'), 'a note',
                    'test', ('apple','orange'), 'a note'),
                ]
        def checker(title, args, outline, exp_title, exp_args, exp_outline):
            tmp = cnt.Container(title, *args, outline=outline)
            self.assertIsInstance(tmp, cnt.Container)
            self.assertEqual(tmp.title, exp_title)
            self.assertEqual(tmp.children, exp_args)
            self.assertEqual(tmp.outline, exp_outline)
        validate_with_fail(self, 'class instance', checker, data)

    def test_inherited(self):
        data = [
                # (title, args, outline, new_title, new_args, new_outline,
                #   exp_title, exp_args, exp_outline)
                (True, 'test', ('a','b',), 'apple',
                    'test2', ('b','c',), 'orange',
                    'test2', ('b','c'), 'orange'),
                ]
        def checker(title, args, outline, new_title, new_args, new_outline, exp_title, exp_args, exp_outline):
            tmp = cnt.Container(title, *args, outline=outline)
            self.assertEqual(tmp.title, title)
            self.assertEqual(tmp.children, args)
            self.assertEqual(tmp.outline, outline)
            tmp2 = tmp.inherited(*new_args, title=new_title, outline=new_outline)
            self.assertIsInstance(tmp2, cnt.Container)
            self.assertEqual(tmp2.title, exp_title)
            self.assertEqual(tmp2.children, exp_args)
            self.assertEqual(tmp2.outline, exp_outline)
        validate_with_fail(self, 'inherited', checker, data)

    #
    # children classes
    #

    def test_children_classes(self):
        data = [
                # (type)
                (True, Story),
                (True, Chapter),
                (True, Episode),
                (True, Scene),
                (False, Material),
                ]
        def checker(ctype):
            tmp = ctype('test', 'a', 'b', 'c', outline='a note')
            self.assertIsInstance(tmp, ctype)
            self.assertEqual(tmp.title, 'test')
            self.assertEqual(tmp.children, ('a', 'b', 'c'))
            self.assertEqual(tmp.outline, 'a note')
        validate_with_fail(self, 'children_classes', checker, data)

    def test_material_class(self):
        tmp = Material(MaterialType.DOCUMENT, 'test', 'a', 'b', 'c', outline='a note')
        self.assertIsInstance(tmp, Material)
        self.assertEqual(tmp.mate_type, MaterialType.DOCUMENT)
        self.assertEqual(tmp.title, 'test')
        self.assertEqual(tmp.children, ('a', 'b', 'c'))
        self.assertEqual(tmp.outline, 'a note')
