# -*- coding: utf-8 -*-
"""Test for subject.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import subject as sb
from builder import info as inf


_FILENAME = "subject.py"


class TestSubject(sb.Subject):

    def __init__(self, name, note):
        super().__init__(name, note)

    def inherited(self):
        return TestSubject(self.name)


class SubjectTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Subject class")

    def setUp(self):
        self.taro = TestSubject("Taro", "a man")

    def test_attributes(self):
        data = [
                ("test", "a note",
                    "test", "a note"),
                ]

        for name, note, exp_name, exp_note in data:
            with self.subTest(name=name, note=note, exp_name=exp_name, exp_note=exp_note):
                tmp = TestSubject(name, note)
                self.assertIsInstance(tmp, sb.Subject)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)

    def test_act(self):
        data = [
                (("test", "apple"), em.ActType.BE, "test",
                    em.ActType.BE, "test",
                    (inf.Info("test"), inf.Info("apple")))
                ]

        for objs, atype, verb, exp_type, exp_verb, exp_objs in data:
            with self.subTest(objs=objs, atype=atype, verb=verb,
                    exp_type=exp_type, exp_verb=exp_verb, exp_objs=exp_objs):
                tmp = self.taro.act(*objs, act_type=atype, verb=verb)
                self.assertIsInstance(tmp, sb.act.Action)
                self.assertEqual(tmp.act_type, exp_type)
                self.assertEqual(tmp.verb, exp_verb)
                self.assertEqual(tmp.objects, exp_objs)

    def test_be(self):
        data = [
                (("test", "apple"),
                    (inf.Info("test"), inf.Info("apple"))),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = self.taro.be(*v)
                self.assertEqual(tmp.act_type, em.ActType.BE)
                self.assertEqual(tmp.verb, "be")
                self.assertEqual(tmp.objects, expected)

    def test_do(self):
        data = [
                (("test", "apple"),
                    (inf.Info("test"), inf.Info("apple"))),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = self.taro.do(*v)
                self.assertEqual(tmp.act_type, em.ActType.DO)
                self.assertEqual(tmp.verb, "do")
                self.assertEqual(tmp.objects, expected)

    def test_explain(self):
        data = [
                (("test", "apple"),
                    (inf.Info("test"), inf.Info("apple"))),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = self.taro.explain(*v)
                self.assertEqual(tmp.act_type, em.ActType.EXPLAIN)
                self.assertEqual(tmp.verb, "explain")
                self.assertEqual(tmp.objects, expected)
