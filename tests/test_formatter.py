# -*- coding: utf-8 -*-
"""Test: formatter.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.formatter import Formatter
from builder.person import Person
from builder.scene import ScenarioType


_FILENAME = "formatter.py"


class FormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Formatter class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")
        self.hana = Person("Hana", "", 15, "female", "flowerlist")

    def test_toDescriptions(self):
        data = [
                (False, ["# test", "## c1", "### e1", "**s1**",
                    "　太郎は学校に行く。"],
                    ["# test\n", "\n## c1\n", "\n### e1\n", "\n**s1**\n",
                        "　太郎は学校に行く。"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toDescriptions(v)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toDescriptions", _checkcode, data)

    def test_toDescriptionsAsEstar(self):
        data = [
                (False, ["# test", "## c1", "### e1", "**s1**",
                    "　太郎は学校に行く。", "「おはよう」", "　彼は言った。"],
                    ["# test\n", "\n## c1\n", "\n### e1\n", "\n**s1**\n",
                        "　太郎は学校に行く。\n", "\n「おはよう」\n", "\n　彼は言った。\n"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toDescriptions(v)
            tmp1 = Formatter().toDescriptionsAsEstar(tmp)
            self.assertIsInstance(tmp1, list)
            self.assertEqual(tmp1, expect)
        validated_testing_withfail(self, "toDescriptionsAsEstar", _checkcode, data)

    def test_toDescriptionsAsLayer(self):
        data = [
                (False, [("__TITLE__", "# test"), ("c1-e1-s1:t1", "　apple。"),
                    ("c1-e1-s1:t2", "　orange。")],
                    ["# test\n", "--------"*8, "## t1\n", "c1-e1-s1: 　apple。",
                        "--------"*8, "## t2\n", "c1-e1-s1: 　orange。"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toDescriptionsAsLayer(v)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toDescriptionsAsLayer", _checkcode, data)

    def test_toDescriptionsAsSmartphone(self):
        data = [
                (False, ["# test", "## c1", "### e1", "**s1**",
                    "　太郎は学校に行く。", "「おはよう」", "　彼は言った。"],
                    ["# test\n", "\n## c1\n", "\n### e1\n", "\n**s1**\n",
                        "　太郎は学校に行く。\n", "「おはよう」\n", "　彼は言った。\n"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toDescriptions(v)
            tmp1 = Formatter().toDescriptionsAsSmartphone(tmp)
            self.assertIsInstance(tmp1, list)
            self.assertEqual(tmp1, expect)
        validated_testing_withfail(self, "toDescriptionsAsEsSmartphone", _checkcode, data)

    def test_toDescriptionsAsWeb(self):
        data = [
                (False, ["# test", "## c1", "### e1", "**s1**",
                    "　太郎は学校に行く。", "「おはよう」", "　彼は言った。"],
                    ["# test\n", "\n## c1\n", "\n### e1\n", "\n**s1**\n",
                        "　太郎は学校に行く。", "\n「おはよう」", "\n　彼は言った。"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toDescriptions(v)
            tmp1 = Formatter().toDescriptionsAsWeb(tmp)
            self.assertIsInstance(tmp1, list)
            self.assertEqual(tmp1, expect)
        validated_testing_withfail(self, "toDescriptionsAsWeb", _checkcode, data)

    def test_toOutlines(self):
        data = [
                (False, ["# test", "## c1", "### e1", "a episode",
                    "**s1**", "a scene"],
                    ["# test\n", "\n## c1\n", "\n### e1\n", "\ta episode\n",
                        "- **s1**: a scene"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toOutlines(v)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toOutlines", _checkcode, data)

    def test_toOutlinesAsLayer(self):
        data = [
                (False, [("__TITLE__", "# test"), ("c1-e1-s1:t1", "apple"),
                    ("c1-e1-s1:t2", "orange")],
                    ["# test\n",
                        "--------"*8,
                        "## t1\n", "c1-e1-s1: apple",
                        "--------"*8,
                        "## t2\n", "c1-e1-s1: orange"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toOutlinesAsLayer(v)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toOutlinesAsLayer", _checkcode, data)

    def test_toScenarios(self):
        data = [
                (False, [(ScenarioType.TITLE, "# test"), (ScenarioType.TITLE, "## c1"),
                    (ScenarioType.TITLE, "### e1"), (ScenarioType.TITLE, "**s1**"),
                    (ScenarioType.PILLAR, "教室:ある日:朝"),
                    (ScenarioType.DIRECTION, "apple"),
                    (ScenarioType.DIALOGUE, "Hana:orange")],
                    ["# test\n", "\n## c1\n", "\n### e1\n", "\n**s1**\n",
                        "○教室（朝）- ある日", "　　apple。", "Hana「orange」"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toScenarios(v)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toScenarios", _checkcode, data)

    def test_toScenariosAsLayer(self):
        data = [
                (False, [("__TITLE__", "", ScenarioType.TITLE, "# test"),
                    ("c1-e1-s1:t1", "教室:ある日:朝", ScenarioType.DIRECTION, "apple"),
                    ("c1-e1-s1:t2", "教室:ある日:朝", ScenarioType.DIALOGUE, "Hana:orange")],
                    ["# test\n",
                        "--------"*8,
                        "## t1\n", "c1-e1-s1: 教室（朝）- ある日", "\tapple。",
                        "--------"*8,
                        "## t2\n", "c1-e1-s1: 教室（朝）- ある日", "Hana「orange」"]),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().toScenariosAsLayer(v)
            self.assertIsInstance(tmp, list)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "toScenarios", _checkcode, data)
