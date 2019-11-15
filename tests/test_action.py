# -*- coding: utf-8 -*-
"""Test: action.py
"""
import unittest
from testutils import print_test_title
from builder.action import Action, ActType, TagAction, TagType
from builder.description import Description, NoDesc, DescType
from builder.flag import Flag, NoFlag, NoDeflag
from builder import __DEF_PRIORITY__, __MIN_PRIORITY__
from builder.person import Person


_FILENAME = "action.py"


class ActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Action class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")

    def test_attributes(self):
        data = [
                (self.taro, "a test", ActType.BE, "test layer",
                    "a test", ActType.BE, "test layer", False),
                (self.taro, "a test", ActType.BE, "test layer",
                    "a test", ActType.BE, "test layer", False),
                (self.taro, "a test", ActType.BE, None,
                    "a test", ActType.BE, Action.DEF_LAYER, False),
                (self.taro, "a test", None, None,
                    "a test", ActType.ACT, Action.DEF_LAYER, False),
                (self.taro, None, None, None,
                    "", ActType.ACT, Action.DEF_LAYER, False),
                (1, "a test", ActType.BE, "test layer",
                    "a test", ActType.BE, "test layer", True),
                (self.taro, 1, ActType.BE, "test layer",
                    "a test", ActType.BE, "test layer", True),
                (self.taro, "a test", 1, "test layer",
                    "a test", ActType.BE, "test layer", True),
                (self.taro, "a test", ActType.BE, 1,
                    "a test", ActType.BE, "test layer", True),
                ]
        def _create(subject, outline, atype, layer):
            if layer:
                return Action(subject, outline, atype, layer)
            elif atype:
                return Action(subject, outline, atype)
            elif outline:
                return Action(subject, outline)
            else:
                return Action(subject)
        def _checkcode(subject, outline1, atype1, layer1, outline2, atype2, layer2):
            tmp = _create(subject, outline1, atype1, layer1)
            self.assertIsInstance(tmp, Action)
            self.assertEqual(tmp.subject, subject)
            self.assertEqual(tmp.outline, outline2)
            self.assertEqual(tmp.act_type, atype2)
            self.assertEqual(tmp.layer, layer2)
            self.assertIsInstance(tmp.description, NoDesc)
            self.assertIsInstance(tmp.getFlag(), NoFlag)
            self.assertIsInstance(tmp.getDeflag(), NoDeflag)
            self.assertEqual(tmp.priority, __DEF_PRIORITY__)
        for subject, outline, atype, layer, exp_outline, exp_atype, exp_layer, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(subject, outline, atype, layer, exp_outline, exp_atype, exp_layer)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(subject, outline, atype, layer, exp_outline, exp_atype, exp_layer)

    def test_setPriority(self):
        data = [
                (1, 1, False),
                (-1, 1, True),
                (100, 1, True),
                ]
        def _checkcode(v, expect):
            tmp = Action(self.taro)
            self.assertEqual(tmp.priority, __DEF_PRIORITY__)
            tmp.setPriority(v)
            self.assertEqual(tmp.priority, expect)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_setLayer(self):
        data = [
                ("test", "test", False),
                (1, "test", True),
                ]
        def _checkcode(v, expect):
            tmp = Action(self.taro)
            self.assertEqual(tmp.layer, Action.DEF_LAYER)
            tmp.setLayer(v)
            self.assertEqual(tmp.layer, expect)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_flag(self):
        data = [
                ("test", "test", False),
                (Flag("test"), "test", False),
                (1, "test", True),
                ]
        def _checkcode(v, expect):
            tmp = Action(self.taro)
            self.assertIsInstance(tmp.getFlag(), NoFlag)
            tmp.flag(v)
            self.assertEqual(tmp.getFlag().info, expect)
            self.assertEqual(tmp.getFlag().isDeflag, False)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_deflag(self):
        data = [
                ("test", "test", False),
                (Flag("test", True), "test", False),
                (1, "test", True),
                ]
        def _checkcode(v, expect):
            tmp = Action(self.taro)
            self.assertIsInstance(tmp.getDeflag(), NoDeflag)
            tmp.deflag(v)
            self.assertEqual(tmp.getDeflag().info, expect)
            self.assertEqual(tmp.getDeflag().isDeflag, True)
        for v, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, expect)

    def test_omit(self):
        data = [
                (__MIN_PRIORITY__, False),
                ]
        def _checkcode(expect):
            tmp = Action(self.taro)
            self.assertEqual(tmp.priority, __DEF_PRIORITY__)
            tmp.omit()
            self.assertEqual(tmp.priority, expect)
        for expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(expect)

    def test_desc(self):
        data = [
                (("test", "apple"), ("test", "apple"), False),
                (("test",), ("test",), False),
                ]
        def _checkcode(vals, expect):
            tmp = Action(self.taro)
            tmp.desc(*vals)
            self.assertEqual(tmp.description.desc_type, DescType.DESC)
            self.assertEqual(tmp.description.descs, expect)
        for vals, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(vals, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(vals, expect)

    def test_tell(self):
        data = [
                (("test", "apple"), ("test", "apple"), False),
                (("test",), ("test",), False),
                ]
        def _checkcode(vals, expect):
            tmp = Action(self.taro)
            tmp.tell(*vals)
            self.assertEqual(tmp.description.desc_type, DescType.DIALOGUE)
            self.assertEqual(tmp.description.descs, expect)
        for vals, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(vals, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(vals, expect)

    def test_comp(self):
        data = [
                (("test", "apple"), ("test", "apple"), False),
                (("test",), ("test",), False),
                ]
        def _checkcode(vals, expect):
            tmp = Action(self.taro)
            tmp.comp(*vals)
            self.assertEqual(tmp.description.desc_type, DescType.COMPLEX)
            self.assertEqual(tmp.description.descs, expect)
        for vals, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(vals, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(vals, expect)

    def test_same(self):
        data = [
                ("test", "d", ("test",), DescType.DESC, False),
                ("test", "t", ("test",), DescType.DIALOGUE, False),
                ("test", "tell", ("test",), DescType.DIALOGUE, False),
                ("test", "c", ("test",), DescType.COMPLEX, False),
                ("test", "comp", ("test",), DescType.COMPLEX, False),
                ("test", None, ("test",), DescType.DESC, False),
                (1, "d", ("test",), DescType.DESC, True),
                ]
        def _checkcode(v, dtype1, expect, dtype2):
            tmp = Action(self.taro, v)
            if dtype1:
                tmp.same(dtype1)
            else:
                tmp.same()
            self.assertEqual(tmp.description.descs, expect)
            self.assertEqual(tmp.description.desc_type, dtype2)
        for v, dtype, expect, exp_dtype, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(v, dtype, expect, exp_dtype)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(v, dtype, expect, exp_dtype)

    def test_inherited(self):
        hanako = Person("Hana", "", 15, "female", "学生")
        base_outline = "a test"
        data = [
                (hanako, "a girl", ("test", "apple"),
                    hanako, "a girl", ("test", "apple"), False),
                (hanako, "a girl", None,
                    hanako, "a girl", (), False),
                (hanako, None, None,
                    hanako, base_outline, (), False),
                (None, None, None,
                    self.taro, base_outline, (), False),
                (1, "a girl", ("test", "apple"),
                    hanako, "a girl", ("test", "apple"), True),
                ]
        def _create(act: Action, subject, outline, desc):
            if desc:
                return act.inherited(subject, outline, desc)
            elif outline:
                return act.inherited(subject, outline)
            elif subject:
                return act.inherited(subject)
            else:
                return act.inherited()
        def _checkcode(subject1, outline1, desc1, subject2, outline2, desc2):
            tmp = Action(self.taro, base_outline)
            _flag = tmp.getFlag()
            _deflag = tmp.getDeflag()
            _pri = tmp.priority
            _layer = tmp.layer
            tmp1 = _create(tmp, subject, outline, desc)
            self.assertIsInstance(tmp1, Action)
            self.assertEqual(tmp1.subject, subject2)
            self.assertEqual(tmp1.outline, outline2)
            self.assertEqual(tmp1.description.descs, desc2)
            self.assertEqual(tmp1.getFlag(), _flag)
            self.assertEqual(tmp1.getDeflag(), _deflag)
            self.assertEqual(tmp1.priority, _pri)
            self.assertEqual(tmp1.layer, _layer)
        for subject, outline, desc, exp_subject, exp_outline, exp_desc, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(subject, outline, desc, exp_subject, exp_outline, exp_desc)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(subject, outline, desc, exp_subject, exp_outline, exp_desc)

class TagActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "TagAction class")

    def test_attributes(self):
        data = [
                ("test", "a test", TagType.COMMENT, TagType.COMMENT, False),
                ("test", "a test", None, TagType.COMMENT, False),
                ("test", "a test", TagType.SYMBOL, TagType.SYMBOL, False),
                (1, "a test", TagType.COMMENT, TagType.COMMENT, True),
                ("test", 1, TagType.COMMENT, TagType.COMMENT, True),
                ("test", "a test", 1, TagType.COMMENT, True),
                ]
        def _checkcode(info, subinfo, ttype, expect):
            tmp = TagAction(info, subinfo, ttype) if ttype else TagAction(info, subinfo)
            self.assertIsInstance(tmp, TagAction)
            self.assertEqual(tmp.info, info)
            self.assertEqual(tmp.subinfo, subinfo)
            self.assertEqual(tmp.tag_type, expect)
        for info, subinfo, ttype, expect, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(info, subinfo, ttype, expect)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(info, subinfo, ttype, expect)

    def test_inherited(self):
        data = [
                ("test", "a test", TagType.BR, False),
                (1, "a test", TagType.BR, True),
                ("test", 1, TagType.BR, True),
                ("test", "a test", 1, True),
                ]
        def _checkcode(info, subinfo, ttype):
            tmp = TagAction(info, subinfo, ttype)
            tmp1 = tmp.inherited()
            self.assertIsInstance(tmp1, TagAction)
            self.assertEqual(tmp1.info, info)
            self.assertEqual(tmp1.subinfo, subinfo)
            self.assertEqual(tmp1.tag_type, ttype)
        for info, subinfo, ttype, isfail in data:
            with self.subTest():
                if not isfail:
                    _checkcode(info, subinfo, ttype)
                else:
                    with self.assertRaises(AssertionError):
                        _checkcode(info, subinfo, ttype)
