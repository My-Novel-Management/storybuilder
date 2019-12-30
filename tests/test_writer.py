# -*- coding: utf-8 -*-
"""Test: writer.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.person import Person
from builder.writer import Writer
from builder.who import Who


_FILENAME = "writer.py"


class WriterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Writer class")

    def setUp(self):
        self.taro = Person("Taro", "山田,太郎", 15, "male", "student")

    def test_attributes(self):
        data = [
                (False, self.taro,),
                ]
        def _checkcode(v):
            tmp = Writer(v)
            self.assertIsInstance(tmp, Writer)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

    ## acts
    def test_be(self):
        data = [
                (False, ("test",), ActType.BE),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).be(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "be", _checkcode, data)

    def test_come(self):
        data = [
                (False, ("test",), ActType.COME),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).come(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "come", _checkcode, data)

    def test_destroy(self):
        data = [
                (False, ("test",), ActType.DESTROY),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).destroy(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "destroy", _checkcode, data)

    def test_go(self):
        data = [
                (False, ("test",), ActType.GO),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).go(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "go", _checkcode, data)

    def test_hear(self):
        data = [
                (False, ("test",), ActType.HEAR),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).hear(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "hear", _checkcode, data)

    def test_look(self):
        data = [
                (False, ("test",), ActType.LOOK),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).look(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "look", _checkcode, data)

    def test_move(self):
        data = [
                (False, ("test",), ActType.MOVE),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).move(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "move", _checkcode, data)

    def test_talk(self):
        data = [
                (False, ("test",), ActType.TALK),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).talk(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "talk", _checkcode, data)

    def test_think(self):
        data = [
                (False, ("test",), ActType.THINK),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).think(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "think", _checkcode, data)

    def test_wear(self):
        data = [
                (False, ("test",), ActType.WEAR),
                ]
        def _checkcode(v, expect):
            tmp = Writer(self.taro).wear(*v)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.act_type, expect)
        validatedTestingWithFail(self, "wear", _checkcode, data)

    ## tags
    def test_br(self):
        data = [
                (False, 1, "1"),
                ]
        def _checkcode(v, expect):
            taro = Writer(self.taro)
            tmp = taro.br(v)
            self.assertEqual(tmp.act_type, ActType.TAG)
            self.assertEqual(tmp.tag_type, TagType.BR)
            self.assertEqual(tmp.note, expect)
        validatedTestingWithFail(self, "br", _checkcode, data)

    def test_comment(self):
        data = [
                (False, "test", "test"),
                ]
        def _checkcode(v, expect):
            taro = Writer(self.taro)
            tmp = taro.comment(v)
            self.assertEqual(tmp.act_type, ActType.TAG)
            self.assertEqual(tmp.tag_type, TagType.COMMENT)
            self.assertEqual(tmp.note, expect)
        validatedTestingWithFail(self, "comment", _checkcode, data)

    def test_hr(self):
        data = [
                (False, 1, 1),
                ]
        def _checkcode(v, expect):
            taro = Writer(self.taro)
            tmp = taro.hr()
            self.assertEqual(tmp.act_type, ActType.TAG)
            self.assertEqual(tmp.tag_type, TagType.HR)
        validatedTestingWithFail(self, "hr", _checkcode, data)

    def test_symbol(self):
        data = [
                (False, "test", "test"),
                ]
        def _checkcode(v, expect):
            taro = Writer(self.taro)
            tmp = taro.symbol(v)
            self.assertEqual(tmp.act_type, ActType.TAG)
            self.assertEqual(tmp.tag_type, TagType.SYMBOL)
            self.assertEqual(tmp.note, expect)
        validatedTestingWithFail(self, "symbol", _checkcode, data)

    def test_title(self):
        data = [
                (False, "test", "test"),
                ]
        def _checkcode(v, expect):
            taro = Writer(self.taro)
            tmp = taro.title(v)
            self.assertEqual(tmp.act_type, ActType.TAG)
            self.assertEqual(tmp.tag_type, TagType.TITLE)
            self.assertEqual(tmp.note, expect)
        validatedTestingWithFail(self, "title", _checkcode, data)

    ## utils
    def test_getWho(self):
        tmp = Writer.getWho()
        self.assertIsInstance(tmp, Writer)
        self.assertIsInstance(tmp.src, Who)
