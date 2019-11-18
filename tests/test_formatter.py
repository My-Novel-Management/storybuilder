# -*- coding: utf-8 -*-
"""Test: formatter.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.formatter import Formatter
from builder.person import Person


_FILENAME = "formatter.py"


class FormatterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Formatter class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")

    def test_asDescription(self):
        data = [
                (False, ["私は食べた", "もりもりと"],
                    "estar", ["私は食べた\n", "もりもりと\n"],),
                (False, ["目の前の大福", "「私は食べた」", "もりもりと"],
                    "estar", ["目の前の大福\n", "\n「私は食べた」\n", "\nもりもりと\n"],),
                (False, ["私は食べた", "もりもりと"],
                    "smart", ["私は食べた\n", "もりもりと\n"],),
                (False, ["目の前の大福", "「私は食べた」", "もりもりと"],
                    "smart", ["目の前の大福\n", "「私は食べた」\n", "もりもりと\n"],),
                (False, ["私は食べた", "もりもりと"],
                    "web", ["私は食べた", "もりもりと"],),
                (False, ["目の前の大福", "「私は食べた」", "もりもりと"],
                    "web", ["目の前の大福", "\n「私は食べた」", "\nもりもりと"],),
                ]
        def _checkcode(v, ftype, expect):
            tmp = Formatter().asDescription(v, ftype)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "asDescription", _checkcode, data)

    def test_asLayer(self):
        from builder.action import Action, TagAction, ActType
        data = [
                (False, ["Title",
                    ("A", "head-data", Action(self.taro, "apple"))],
                    True, ["Title", "--------"*9 + f"\n## A\n",
                        "head-data: apple"],),
                (False, ["Title",
                    ("A", "head-data", Action(self.taro, "apple", ActType.TALK))],
                    True, ["Title", "--------"*9 + f"\n## A\n",
                        "head-data: _「apple」_"],),
                (False, ["Title",
                    ("A", "head-data", Action(self.taro, "apple").d("orange"))],
                    False, ["Title", "--------"*9 + f"\n## A\n",
                        "head-data: orange"],),
                (False, ["Title",
                    ("A", "head-data", Action(self.taro, "apple", ActType.TALK).t("orange"))],
                    False, ["Title", "--------"*9 + f"\n## A\n",
                        "head-data: _「orange」_"],),
                (False, ["Title",
                    ("A", "head-data", Action(self.taro, "apple").t("orange"))],
                    False, ["Title", "--------"*9 + f"\n## A\n",
                        "head-data: _「orange」_"],),
                ]
        def _checkcode(v, isOutline, expect):
            tmp = Formatter().asLayer(v, isOutline)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "asLayer", _checkcode, data)

    def test_asOutline(self):
        data = [
                (False, [("### test", "apple"),],
                    ["### test\n\n\tapple",],),
                (False, [("## test", "apple"),],
                    ["## test",],),
                (False, [("# test", "apple"),],
                    ["# test",],),
                (False, [("test", "apple"),],
                    ["- 「test」: apple",],),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().asOutline(v)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "asOutline", _checkcode, data)

    def test_asScenario(self):
        from builder.scene import ScenarioType
        data = [
                (False, [(ScenarioType.DIRECTION, "test"),],
                    ["　　test"],),
                (False, [(ScenarioType.DIALOGUE, "test"),],
                    ["test"],),
                ]
        def _checkcode(v, expect):
            tmp = Formatter().asScenario(v)
            self.assertEqual(tmp, expect)
        validated_testing_withfail(self, "asScenario", _checkcode, data)

