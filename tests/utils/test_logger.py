# -*- coding: utf-8 -*-
'''
MyLogger class test
===================
'''

import unittest
from testutils import print_testtitle, validate_with_fail
from builder.utils import logger


class MyLoggerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(logger.__name__, 'MyLogger class')

    def test_instance(self):
        data = [
                # (name, sh, fh)
                (True, "test", "%(message)", "%(message)"),
                ]
        def checker(name, sh, fh):
            _ = logger.MyLogger(name, sh, fh)
            self.assertIsInstance(_, logger.MyLogger)
            self.assertEqual(_.name, name)
        validate_with_fail(self, 'class-instance', checker, data)

    def test_static_get_logger(self):
        data = [
                # (name, sh, fh)
                (True, "test", '%(message)', '%(message)'),
                ]
        def checker(name, sh, fh):
            _ = logger.MyLogger.get_logger(name, sh, fh)
            self.assertIsInstance(_, logger.MyLogger)
            self.assertEqual(_.name, name)
            _
        validate_with_fail(self, 'staticmethod-get_logger', checker, data)

