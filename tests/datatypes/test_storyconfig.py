# -*- coding: utf-8 -*-
'''
StoryConfig class test
======================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes import storyconfig as sc


class StoryConfigTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(sc.__name__, 'StoryConfig class')

    def test_instance(self):
        data = [
                # (title, expect)
                (True, 'test', 'test'),
                ]
        def checker(title, expect):
            tmp = sc.StoryConfig(title)
            self.assertIsInstance(tmp, sc.StoryConfig)
            self.assertEqual(tmp.title, expect)
        validate_with_fail(self, 'class instance', checker, data)
