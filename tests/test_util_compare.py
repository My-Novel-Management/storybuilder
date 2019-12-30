# -*- coding: utf-8 -*-
"""Test: util_compare.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
import utils.util_compare as util
from builder.chapter import Chapter
from builder.episode import Episode
from builder.scene import Scene
from builder.story import Story


_FILENAME = "util_comapre.py"


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "util compare methods")

    def setUp(self):
        pass

    def test_equalsContainers(self):
        data = [
                (False, Story("test"), Story("test"), True),
                (False, Story("test"), Story("apple"), False),
                (False, Chapter("test"), Chapter("test"), True),
                (False, Chapter("test"), Episode("test"), False),
                ]
        def _checkcode(v1, v2, expect):
            self.assertEqual(util.equalsContainers(v1,v2), expect)
        validatedTestingWithFail(self, "equalsContainers", _checkcode, data)

    def test_equalsContainerLists(self):
        ch1, ch2, ch3 = Chapter("1"), Chapter("2"), Chapter("3")
        data = [
                (False, (ch1, ch2), (ch1,ch2), True),
                (False, (ch1, ch2), (ch1,ch3), False),
                ]
        def _checkcode(v1, v2, expect):
            self.assertEqual(util.equalsContainerLists(v1, v2), expect)
        validatedTestingWithFail(self, "equalsContainerLists", _checkcode, data)
