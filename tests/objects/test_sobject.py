# -*- coding: utf-8 -*-
'''
SObject class test
==================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder import __PRIORITY_DEFAULT__, __PRIORITY_MIN__
from builder.objects import sobject as sobj


class SObjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(sobj.__name__, 'SObject class')

    def test_instance(self):
        data = [
                # (name, expect, exp_pri)
                (True, 'test', 'test', __PRIORITY_DEFAULT__),
                ]
        def checker(name, expect, exp_pri):
            tmp = sobj.SObject(name)
            self.assertIsInstance(tmp, sobj.SObject)
            self.assertEqual(tmp.name, expect)
            self.assertEqual(tmp.priority, exp_pri)
        validate_with_fail(self, 'class instance', checker, data)

    def test_omit(self):
        data = [
                # (name, expect)
                (True, 'test', __PRIORITY_MIN__),
                ]
        def checker(name, expect):
            tmp = sobj.SObject(name)
            self.assertEqual(tmp.priority, __PRIORITY_DEFAULT__)
            tmp.omit()
            self.assertEqual(tmp.priority, expect)
        validate_with_fail(self, 'omit', checker, data)

