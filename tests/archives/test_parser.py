# -*- coding: utf-8 -*-
"""Test: parser.py
"""
import unittest
from builder.testutils import print_test_title
from builder import action as act
from builder import parser as ps
from builder import person as psn
from builder import item as itm
from builder import info as inf
from builder import enums as em
from builder import world as wd


_FILENAME = "parser.py"


class PublicMethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "public methods")

    def setUp(self):
        self.taro = psn.Person("Taro", 17, "male", "student")
        self.hanako = psn.Person("Hanako", 17, "female", "student")
        self.box = itm.Item("Box", "a box")
        self.test = inf.Info("Test")
        self.something = inf.Something()
        self.tag_br = act.TagAction(em.TagType.BR, "")
        self.tag_h1 = act.TagAction(em.TagType.HEAD1, "test")
        self.tag_h2 = act.TagAction(em.TagType.HEAD2, "test")
        self.tag_h3 = act.TagAction(em.TagType.HEAD3, "test")

    def test_actinfo_from_action(self):
        data = [
                (self.taro.be(), 0, em.LangType.ENG, False,
                    "- Taro    :be          /"),
                (self.taro.have(self.box), 0, em.LangType.ENG, False,
                    "- Taro    :have        /Box"),
                (self.taro.do(self.test), 0, em.LangType.ENG, False,
                    "- Taro    :do          /Test"),
                (self.taro.talk(self.something), 1, em.LangType.ENG, False,
                    "    - Taro    :talk        /X"),
                (self.taro.ask(self.hanako, self.test), 0, em.LangType.ENG, False,
                    "- Taro    :ask         /Hanako/Test"),
                ]

        for v, lv, lang, dbg, expected in data:
            with self.subTest(v=v, lv=lv, lang=lang, dbg=dbg, expected=expected):
                self.assertEqual(ps.actinfo_from_action(v, lv, lang, dbg), expected)

    def test_actinfo_from_tag(self):
        data = [
                (self.tag_br, "\n"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.actinfo_from_tag(v), expected)

    def test_actobject_name_of(self):
        data = [
                (self.taro,
                    "Taro"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.actobject_name_of(v), expected)

    def test_actobject_names_from(self):
        data = [
                (self.taro.be(self.box),
                    "Box"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.actobject_names_from(v), expected)

    def test_description_from_action(self):
        data = [
                (self.taro.be().d("test"), em.LangType.ENG,
                    "test."),
                (self.taro.be().d("test"), em.LangType.JPN,
                    "test。"),
                (self.taro.be().t("test"), em.LangType.ENG,
                    '"test"'),
                (self.taro.be().t("test"), em.LangType.JPN,
                    "「test」"),
                (self.taro.be().pre("test"), em.LangType.ENG,
                    "test"),
                (self.taro.be().pre("test"), em.LangType.JPN,
                    "test"),
                ]

        for v, lang, expected in data:
            with self.subTest(v=v, lang=lang, expected=expected):
                self.assertEqual(ps.description_from_action(v, lang), expected)

    def test_description_from_tag(self):
        data = [
                (self.tag_br,
                    "\n"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.description_from_tag(v), expected)

    def test_scene_gathered_from(self):
        w = wd.World("test")
        data = [
                ((w.scene("test"),),
                    1),
                ((w.scene("test"), w.scene("apple")),
                    2),
                ((w.chaptertitle("test"), self.taro.be()),
                    0),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = ps.scenes_gathered_from(v)
                self.assertEqual(len(tmp), expected)

    def test_story_filtered_by_priority(self):
        taro = self.taro.be()
        hanako = self.hanako.be()
        group = act.ActionGroup(taro, hanako,
                group_type=em.GroupType.SCENE)
        data = [
                ((self.taro.be(), self.hanako.be().omit(),),
                    5,
                    (self.taro.be(),)),
                ((self.taro.be(),
                    act.ActionGroup(taro, hanako, group_type=em.GroupType.SCENE),),
                    5,
                    (self.taro.be(),
                        act.ActionGroup(taro, hanako, group_type=em.GroupType.SCENE)),),
                ((self.taro.be(),
                    act.ActionGroup(taro, group_type=em.GroupType.SCENE).omit()),
                    5,
                    (self.taro.be(),)),
                ]

        for v, pri, expected in data:
            with self.subTest(v=v, pri=pri, expected=expected):
                tmp = ps.story_filtered_by_priority(v, pri)
                for res, exp in zip(tmp, expected):
                    if hasattr(res, "subject"):
                        self.assertEqual(res, exp)
                    else:
                        self.assertEqual(res.actions, exp.actions)

    def test_str_to_dict_by_splitter(self):
        data = [
                ("a:b:c:d", "test", "apple",
                    {"a":"b", "c":"d", "test":"apple"}),
                ]

        for v, dkey, dval, expected in data:
            with self.subTest(v=v, dkey=dkey, dval=dval, expected=expected):
                self.assertEqual(ps.str_to_dict_by_splitter(v, dkey, dval), expected)

    def test_str_to_tuple_from_args(self):
        data = [
                (("test",),
                    ("test",)),
                (("test", "apple"),
                    ("test", "apple")),
                ("test",
                    ("test",)),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.str_to_tuple_from_args(v), expected)

    def test_subjects_retrieved_from(self):
        data = [
                ((self.taro.be(),), psn.Person,
                    (self.taro,)),
                ((self.taro.talk(self.hanako),), psn.Person,
                    (self.taro, self.hanako)),
                ]

        for v, cls, expected in data:
            with self.subTest(v=v, cls=cls, expected=expected):
                self.assertEqual(ps.subjects_retrieved_from(v, cls), list(expected))

    def test_title_level_of(self):
        data = [
                (em.TagType.HEAD1, 1),
                (em.TagType.HEAD2, 2),
                (em.TagType.HEAD3, 3),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.title_level_of(v), expected)

    def titles_retrieved_from(self):
        data = [
                ((self.taro.be(),),
                    ()),
                ((self.taro.be(), self.tag_h1),
                    (self.tag_h1,)),
                ((self.taro.be(), self.tag_h2, self.tag_h3,),
                    (self.tag_h2, self.tag_h3)),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.titles_retrieved_from(v), expected)

    def test_verb_from(self):
        data = [
                (self.taro.be(),
                    "be"),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                self.assertEqual(ps.verb_from(v), expected)

    def test_word_dictionary_from(self):
        data = [
                ("item", ("test", "item1"),
                    ("test", "item1")),
                ("info", ("test", "info1"),
                    ("i_test", "info1")),
                ("stage", ("test", "stage1"),
                    ("st_test", "stage1")),
                ("person", ("test", "Taro", 17, "male", "student"),
                    ("n_test", "Taro")),
                ("person", ("test2", "Tanaka,Taro", 17, "male", "student"),
                    ("fn_test2", "Taro")),
                ("person", ("test3", "Tanaka,Taro", 17, "male", "student"),
                    ("ln_test3", "Tanaka")),
                ]
        def creator(w: wd.World, cls, val):
            if cls == 'item':
                return w.append_item(val[0], val[1:])
            elif cls == 'stage':
                return w.append_stage(val[0], val[1:])
            elif cls == 'person':
                return w.append_person(val[0], val[1:])
            else:
                return w.append_info(val[0], val[1:])

        for cls, v, expected in data:
            with self.subTest(cls=cls, v=v, expected=expected):
                tmp = wd.World("dict test")
                creator(tmp, cls, v)
                result = ps.word_dictionary_from(tmp)
                self.assertIsInstance(result, dict)
                self.assertEqual(result[expected[0]], expected[1])

