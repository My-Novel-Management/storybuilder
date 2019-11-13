# -*- coding: utf-8 -*-
"""Test for action.py
"""
import unittest
from builder.testutils import print_test_title
from builder import action as act
from builder import enums as em
from builder import item as it


_FILENAME = "action.py"


class ActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Action")

    def setUp(self):
        self.taro = it.Item("Test", "a box")
        self.act = act.Action(em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, ())

    def test_attributes(self):
        data = [
                (em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, (),
                    em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, ()),
                ]
        for atype, sub, verb, aux, obj, exp_type, exp_sub, exp_verb, exp_aux, exp_obj in data:
            with self.subTest(atype=atype, sub=sub, verb=verb, aux=aux, obj=obj,
                    exp_type=exp_type, exp_sub=exp_sub, exp_verb=exp_verb, exp_aux=exp_aux, exp_obj=exp_obj):
                tmp = act.Action(atype, sub, verb, aux, obj)
                self.assertIsInstance(tmp, act.Action)
                self.assertEqual(tmp.act_type, exp_type)
                self.assertEqual(tmp.subject, exp_sub)
                self.assertEqual(tmp.verb, exp_verb)
                self.assertEqual(tmp.objects, exp_obj)
                self.assertIsInstance(tmp.description, act.ds.NoDesc)
                self.assertEqual(tmp.auxverb, exp_aux)
                self.assertEqual(tmp.priority, act.Action.PRIORITY_DEFAULT)

    def test_desc(self):
        data = [
                (("test",), ("test",)),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = act.Action(em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, ())
                self.assertIsInstance(tmp.desc(*v).description, act.ds.Desc)
                self.assertEqual(tmp.description.data, expected)

    def test_tell(self):
        data = [
                (("test",), ("test",)),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = act.Action(em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, ())
                self.assertIsInstance(tmp.tell(*v).description, act.ds.Desc)
                self.assertEqual(tmp.description.data, expected)

    def test_pre(self):
        data = [
                (("test",), ("test",)),
                ]
        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = act.Action(em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, ())
                self.assertIsInstance(tmp.pre(*v).description, act.ds.Desc)
                self.assertEqual(tmp.description.data, expected)


class ActionGroupTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "ActionGroup")

    def setUp(self):
        self.taro = it.Item("Test", "a box")
        self.act = act.Action(em.ActType.BE, self.taro, "be", em.AuxVerb.NONE, ())

    def test_attributes(self):
        data = [
                ((self.act,), em.GroupType.SCENE, em.LangType.JPN,
                    em.GroupType.SCENE, em.LangType.JPN, (self.act,)),
                ]

        for acts, group, lang, exp_group, exp_lang, exp_acts in data:
            with self.subTest(acts=acts, group=group, lang=lang,
                    exp_group=exp_group, exp_lang=exp_lang, exp_acts=exp_acts):
                tmp = act.ActionGroup(group_type=group, lang=lang, *acts)
                self.assertIsInstance(tmp, act.ActionGroup)
                self.assertEqual(tmp.group_type, exp_group)
                self.assertEqual(tmp.lang, exp_lang)
                self.assertEqual(tmp.actions, exp_acts)


class TagActionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "TagAction")

    def test_attributes(self):
        data = [
                (em.TagType.COMMENT, "test",
                    em.TagType.COMMENT, "test"),
                (em.TagType.BR, "",
                    em.TagType.BR, ""),
                (em.TagType.HR, "hr",
                    em.TagType.HR, "hr"),
                (em.TagType.SYMBOL, "*",
                    em.TagType.SYMBOL, "*"),
                (em.TagType.HEAD1, "test",
                    em.TagType.HEAD1, "test"),
                (em.TagType.HEAD2, "test",
                    em.TagType.HEAD2, "test"),
                (em.TagType.HEAD3, "test",
                    em.TagType.HEAD3, "test"),
                ]

        for tag, info, exp_tag, exp_info in data:
            with self.subTest(tag=tag, info=info, exp_tag=exp_tag, exp_info=exp_info):
                tmp = act.TagAction(tag, info)
                self.assertIsInstance(tmp, act.TagAction)
                self.assertEqual(tmp.act_type, em.ActType.TAG)
                self.assertEqual(tmp.tag, exp_tag)
                self.assertEqual(tmp.info, exp_info)

