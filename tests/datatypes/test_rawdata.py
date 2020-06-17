# -*- coding: utf-8 -*-
'''
RawData class test
==================
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.datatypes.formattag import FormatTag
from builder.datatypes import rawdata as rd


class RawDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(rd.__name__, 'RawData class')

    def test_instance(self):
        data = [
                # (args, expect)
                (True, ('a', 'b', FormatTag.DESCRIPTION_HEAD),
                    ('a', 'b', FormatTag.DESCRIPTION_HEAD)),
                ]
        def checker(args, expect):
            tmp = rd.RawData(*args)
            self.assertIsInstance(tmp, rd.RawData)
            self.assertEqual(tmp.data, expect)
        validate_with_fail(self, 'instance', checker, data)

