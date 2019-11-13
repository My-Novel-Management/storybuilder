# -*- coding: utf-8 -*-
"""Test for analyzer.py
"""
import unittest
from builder.testutils import print_test_title
from builder import action as act
from builder import enums as em
from builder import person as psn
from builder import item as itm
from builder import info as inf
from builder import analyzer as ayz


_FILENAME = "analyzer.py"


class PublicMethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "public methods")

    def setUp(self):
        self.taro = psn.Person("Taro", 17, "male", "student")
        self.hanako = psn.Person("Hanako", 17, "female", "student")
        self.box = itm.Item("Box", "a box")
        self.stick = itm.Item("Stick", "a stick")

    def test_contains_the_action_in(self):
        data = [
                ((self.taro.be(self.box),),
                    self.taro.be(self.box), True),
                ((self.taro.be(self.box),),
                    self.taro.be(), True),
                ((self.taro.be(),),
                    self.taro.be(self.box), False),
                ((self.taro.be(self.box),),
                    self.taro.be(inf.Something()), True),
                ((self.taro.be(self.box, inf.Something()),),
                    self.taro.be(self.box, self.stick), True),
                ]

        for v, target, expected in data:
            with self.subTest(v=v, target=target, expected=expected):
                self.assertEqual(ayz.contains_the_action_in(v, target), expected)

    def test_count_acttypes(self):
        data = [
                ((self.taro.be(),),
                    em.ActType.BE, 1),
                ((self.taro.be(), self.taro.do(), self.taro.do()),
                    em.ActType.DO, 2),
                ]

        for v, atype, expected in data:
            with self.subTest(v=v, atype=atype, expected=expected):
                tmp = ayz.count_acttypes(v)
                self.assertIsInstance(tmp, dict)
                self.assertEqual(tmp[atype], expected)

    def test_count_description_at_action(self):
        data = [
                (self.taro.be().d("test"),
                    False, 4),
                (self.taro.be().d("test", "apple"),
                    False, 9),
                (self.taro.be().d("test", "apple"),
                    True, 11),
                ]

        for v, strict, expected in data:
            with self.subTest(v=v, strict=strict, expected=expected):
                self.assertEqual(ayz.count_descripton_at_action(v, strict), expected)

    def test_count_subjects_in(self):
        taro1 = self.taro.be("test")
        data = [
                ((taro1,),
                    psn.Person, 1),
                ((inf.Something(), inf.Info("test")),
                    inf.Something, 1),
                ]

        for v, target, expected in data:
            with self.subTest(v=v, target=target, expected=expected):
                self.assertEqual(ayz.count_subjects_in(v, target), expected)

    def test_has_a_subject_in(self):
        data = [
                ((self.taro.be(),),
                    psn.Person, True),
                ((self.taro.be(),),
                    itm.Item, False),
                ((self.taro.have(self.box),),
                    itm.Item, True),
                ]

        for v, cls, expected in data:
            with self.subTest(v=v, cls=cls, expected=expected):
                self.assertEqual(ayz.has_a_subject_in(v, cls), expected)

    def test_has_the_action_in(self):
        data = [
                ((self.taro.be(),),
                    self.taro.be(), True),
                ]

        for v, target, expected in data:
            with self.subTest(v=v, target=target, expected=expected):
                self.assertEqual(ayz.has_the_action_in(v, target), expected)

    def test_has_the_keyword(self):
        data = [
                ((self.taro.be(),),
                    "Taro", False, True),
                ((self.taro.be(),),
                    "Hanako", False, False),
                ((self.taro.be(), self.hanako.be(),),
                    "Ta", False, True),
                ((self.taro.talk(self.hanako),),
                    "Hanako", False, True),
                ((self.hanako.ask(self.taro),),
                    "Ta", True, False),
                ]

        for v, target, strict, expected in data:
            with self.subTest(v=v, target=target, strict=strict, expected=expected):
                self.assertEqual(ayz.has_the_keyword(v, target, strict), expected)

    def test_has_the_keyword_in_description(self):
        data = [
                ((self.taro.be().d("test"),),
                    "test", True),
                ((self.taro.be().d("apple"),),
                    "test", False),
                ((self.taro.be().d("testing"),),
                    "test", True),
                ]

        for v, target, expected in data:
            with self.subTest(v=v, target=target, expected=expected):
                self.assertEqual(ayz.has_the_keyword_in_descriptions(v, target), expected)

    def test_has_the_subject_in(self):
        data = [
                ((self.taro.be(),),
                    self.taro, True),
                ]

        for v, target, expected in data:
            with self.subTest(v=v, target=target, expected=expected):
                self.assertEqual(ayz.has_the_subject_in(v, target), expected)
