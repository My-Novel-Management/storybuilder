# -*- coding: utf-8 -*-
"""Test utility.
"""
import unittest


# public methods
def print_test_title(fname: str, title: str) -> bool:
    assert isinstance(fname, str)
    assert isinstance(title, str)

    print("\n**** TEST: {} - {} ****".format(fname, title))

    return True

def validated_testing_withfail(testcase: unittest.TestCase,
        title: str, testfunc, data: list):
    for vals in data:
        with testcase.subTest(title=title):
            assert isinstance(vals[0], bool)
            if not vals[0]:
                testfunc(*vals[1:])
            else:
                with testcase.assertRaises((AssertionError, TypeError)):
                    testfunc(*vals[1:])
