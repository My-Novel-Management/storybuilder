# -*- coding: utf-8 -*-
"""Test for enums.py
"""
import unittest
from builder.sbutils import print_test_title
from builder.enums import ActType, AuxVerb, DescType, GroupType, LangType, TagType


_FILENAME = "enums.py"


class EnumsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Enums(ActType)")

    def test_act_type(self):
        data = sorted([
                "BE",
                "BEHAV",
                "DEAL",
                "DO",
                "EXPLAIN",
                "FEEL",
                "GROUP",
                "LOOK",
                "MOVE",
                "TAG",
                "TALK",
                "TEST",
                "THINK",
                ])
        idx = 0
        for act in ActType:
            self.assertEqual(str(act), data[idx])
            idx += 1

    def test_auxverb(self):
        data = sorted([
                "CAN",
                "MAY",
                "MUST",
                "NONE",
                "SHOULD",
                "WANT",
                "WILL"
                ])

        idx = 0
        for aux in AuxVerb:
            self.assertEqual(str(aux), data[idx])
            idx += 1

    def test_desc_type(self):
        data = sorted([
                "_DESCRIPTION",
                "_DIALOGUE",
                "_NONE",
                "_TAG"
                ])
        idx = 0
        for d in DescType:
            self.assertEqual(str(d), data[idx])
            idx += 1

    def test_group_type(self):
        data = sorted([
                "_COMBI",
                "_SCENE",
                "_STORY"
                ])
        idx = 0
        for g in GroupType:
            self.assertEqual(str(g), data[idx])
            idx += 1

    def test_lang_type(self):
        data = sorted([
                "_ENG",
                "_JPN",
                ])
        idx = 0
        for l in LangType:
            self.assertEqual(str(l), data[idx])
            idx += 1

    def test_tag_type(self):
        data = sorted([
                "_BR",
                "_COMMENT",
                "_HR",
                "_NONE",
                "_TITLE",
                "_SYMBOL",
                ])
        idx = 0
        for t in TagType:
            self.assertEqual(str(t), data[idx])
            idx += 1

