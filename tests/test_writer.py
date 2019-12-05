# -*- coding: utf-8 -*-
"""Test: writer.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.action import Action
from builder.writer import Writer, Does
from builder.person import Person
from builder.who import Who


_FILENAME = "writer.py"


class WriterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Writer class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student", "me:俺")
        self.hana = Person("Hana", "", 15, "female", "student", "me:私")

    def test_attributes(self):
        tmp = Writer(self.taro)
        self.assertIsInstance(tmp, Writer)
        self.assertEqual(tmp.subject, self.taro)

    def test_do(self):
        data = [
                (False, self.taro, None, "test", self.taro, "Taroはtest"),
                (False, None, None, "test", Who(), "test"),
                (False, self.taro, self.hana, "test", self.hana, "Hanaはtest"),
                ]
        def _checkcode(p1, p2, v, exp1, exp2):
            tmp = Writer(p1) if p1 else Writer()
            tmp1 = tmp.do(v, p2) if p2 else tmp.do(v)
            self.assertIsInstance(tmp1, Action)
            self.assertEqual(tmp1.subject, exp1)
            self.assertEqual(tmp1.outline, exp2)
        validated_testing_withfail(self, "do", _checkcode, data)

    def test_be(self):
        data = [
                (False, self.taro, None, None, f"Taroは{Does.BE.value}"),
                (False, self.taro, "test", None, f"Taroはtest{Does.BE.value}"),
                ]
        def _be(w, v, obj):
            if obj:
                return w.be(v, obj)
            elif v:
                return w.be(v)
            else:
                return w.be()
        def _checkcode(p, v, obj, expect):
            tmp = Writer(p) if p else Writer()
            tmp1 = _be(tmp, v, obj)
            self.assertIsInstance(tmp1, Action)
            self.assertEqual(tmp1.subject, p)
            self.assertEqual(tmp1.outline, expect)
        validated_testing_withfail(self, "be", _checkcode, data)

    def test_does(self):
        tmp = Writer(self.taro)
        for v in Does:
            atr = v.name.lower()
            with self.subTest(atr=atr):
                self.assertTrue(hasattr(tmp, atr))
