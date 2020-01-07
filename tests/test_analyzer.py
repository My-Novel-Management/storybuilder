# -*- coding: utf-8 -*-
"""Test: analyzer.py
"""
## public libs
import unittest
## third libs
import MeCab
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import WordClasses
from builder.action import Action
from builder.analyzer import Analyzer
from builder.chapter import Chapter
from builder.episode import Episode
from builder.scene import Scene
from builder.story import Story


_FILENAME = "analyzer.py"


class AnalyzerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Analyzer class")

    def setUp(self):
        self.anal = Analyzer("")
        pass

    def test_attributes(self):
        tmp = Analyzer("")
        self.assertIsInstance(tmp, Analyzer)

    def test_collectionsWordClassByMeCab(self):
        data = [
                (False, Story("test", Chapter("c1", Episode("e1",
                    Scene("s1",
                        Action("雨が降る"))))),
                    WordClasses.NOUN,
                    [["雨","名詞","一般","*","*","*","*","雨","アメ","アメ"]]),
                ]
        def _checkcode(v, wcls, expect):
            tmp = self.anal.collectionsWordClassByMecab(v)
            self.assertEqual(tmp[wcls.name], expect)
        validatedTestingWithFail(self, "collectionsWordClassByMeCab", _checkcode, data)

    def test_verbs(self):
        data = [
                (False, "雨が降る夜",
                    ["降る"]),
                (False, "雨が降る夜に出会う",
                    ["降る", "出る"]),
                (False, ("雨が降る", "夜に会う"),
                    ["降る", "会う"]),
                ]
        validatedTestingWithFail(self, "verbs", lambda v,expect: self.assertEqual(
            self.anal.verbs(v), expect), data)
