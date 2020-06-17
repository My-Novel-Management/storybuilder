# -*- coding: utf-8 -*-
'''
World class test
================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder import world as wd


class WorldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(wd.__name__, 'World class')

    def test_instance(self):
        data = [
                # (title, expect)
                (True, 'test', 'test'),
                ]
        def checker(title, expect):
            tmp = wd.World(title)
            self.assertIsInstance(tmp, wd.World)
            self.assertEqual(tmp.config.title, expect)
        validate_with_fail(self, 'class instance', checker, data)

