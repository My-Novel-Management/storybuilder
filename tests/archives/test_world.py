# -*- coding: utf-8 -*-
"""Test: world.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import world as wd


_FILENAME = "world.py"


class AuxverbDictTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "AuxverbDict class")

    def test_attributes(self):
        data = [
                ("can", em.AuxVerb.CAN),
                ("may", em.AuxVerb.MAY),
                ("must", em.AuxVerb.MUST),
                ("none", em.AuxVerb.NONE),
                ("should", em.AuxVerb.SHOULD),
                ("want", em.AuxVerb.WANT),
                ("will", em.AuxVerb.WILL),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = wd.AuxverbDict()
                self.assertEqual(getattr(tmp, v), expected)


class SDictTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "SDict class")

    def test_attributes(self):
        tmp = wd.SDict()
        tmp["test"] = "apple"
        self.assertTrue(hasattr(tmp, "test"))


class TagManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "TagManager class")

    def test_attributes(self):
        data = [
                ("br", None, None, em.TagType.BR, ""),
                ("comment", "test", None, em.TagType.COMMENT, "test"),
                ("hr", None, None, em.TagType.HR, ""),
                ("symbol", "*", None, em.TagType.SYMBOL, "*"),
                ("title", "test", 1, em.TagType.HEAD1, "test"),
                ("title", "test", 2, em.TagType.HEAD2, "test"),
                ("title", "test", 3, em.TagType.HEAD3, "test"),
                ]

        for v, info, lv, exp_tag, expected in data:
            with self.subTest(v=v, info=info, lv=lv, exp_tag=exp_tag, expected=expected):
                t = wd.TagManager()
                doing = getattr(t, v)
                tmp = doing(info, lv) if info and lv else (doing(info) if info else doing())
                self.assertEqual(tmp.tag, exp_tag)
                self.assertEqual(tmp.info, expected)


class WorldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "World class")

    def test_attributes(self):
        data = [
                ("test", "a note", None,
                    "test", "a note", em.LangType.JPN),
                ]

        for name, note, lang, exp_name, exp_note, exp_lang in data:
            with self.subTest(name=name, note=note, lang=lang, exp_name=exp_name,
                    exp_note=exp_note, exp_lang=exp_lang):
                tmp = wd.World(name, note, lang) if lang else wd.World(name, note)
                self.assertIsInstance(tmp, wd.World)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)
                self.assertEqual(tmp.lang, exp_lang)
