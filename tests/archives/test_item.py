# -*- coding: utf-8 -*-
"""Test for item.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import item as it
from builder import info as inf


_FILENAME = "item.py"


class ItemTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Item class")

    def setUp(self):
        self.box = it.Item("Test", "a box")

    def test_attributes(self):
        data = [
                ("test", "a note",
                    "test", "a note"),
                ("test", "",
                    "test", ""),
                ]
        for name, note, exp_name, exp_note in data:
            with self.subTest(name=name, note=note, exp_name=exp_name, exp_note=exp_note):
                tmp = it.Item(name, note) if note else it.Item(name)
                self.assertIsInstance(tmp, it.Item)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)

    def test_move(self):
        data = [
                (("test", "apple"),
                    (inf.Info("test"), inf.Info("apple"))),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = self.box.move(*v)
                self.assertIsInstance(tmp, it.sb.act.Action)
                self.assertEqual(tmp.act_type, em.ActType.MOVE)
                self.assertEqual(tmp.subject, self.box)
                self.assertEqual(tmp.verb, "move")
                self.assertEqual(tmp.objects, expected)


