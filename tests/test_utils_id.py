# -*- coding: utf-8 -*-
"""Test: util_id.py
"""
import unittest
from testutils import printTestTitle, validatedTestingWithFail
from utils import util_id


_FILENAME = "util_id.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "id utility")

    def test_getNextId(self):
        tmp = util_id.UtilityID.getNextId()
        self.assertIsInstance(tmp, int)
