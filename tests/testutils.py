# -*- coding: utf-8 -*-
'''
Utility methods for test
========================
'''

__all__ = ('print_testtitle', 'validate_with_fail')

from typing import Callable
import unittest


def print_testtitle(fname: str, title: str) -> None:
    ''' Print test title.
    '''
    assert isinstance(fname, str)
    assert isinstance(title, str)

    print(f"\n======== TEST: [ {fname} ] - {title} ========")


def validate_with_fail(testcase: unittest.TestCase, title: str,
        testfunc: Callable, data: list) -> None:
    ''' Useful test function, the test run and get a success if that contains
            AssertionError or TypeError.
    Usage:
        >>> data = [
                    (True, dataA, dataB, dataC),
                    (False, dataA, dataB, dataC), # if error is expected
                ]
        >>> validate_with_fail(testcase, testfunc, data)
    '''
    assert isinstance(testcase, unittest.TestCase)
    assert isinstance(title, str)
    assert callable(testfunc)
    assert isinstance(data, list)

    for vals in data:
        with testcase.subTest(title=title, vals=vals):
            assert isinstance(vals[0], bool)
            if vals[0]:
                testfunc(*vals[1:])
            else:
                with testcase.assertRaises((AssertionError, TypeError)):
                    testfunc(*vals[1:])

