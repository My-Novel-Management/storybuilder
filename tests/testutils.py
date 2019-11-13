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

