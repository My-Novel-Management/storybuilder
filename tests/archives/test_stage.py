# -*- coding: utf-8 -*-
"""Test for stage.py
"""
import unittest
from builder.testutils import print_test_title
from builder import enums as em
from builder import stage as st
from builder import info as inf


_FILENAME = "stage.py"


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Item class")

    def setUp(self):
        self.bus = st.Stage("Test", "a bus")

    def test_attributes(self):
        data = [
                ("test", "a note",
                    "test", "a note"),
                ("test", "",
                    "test", ""),
                ]
        for name, note, exp_name, exp_note in data:
            with self.subTest(name=name, note=note, exp_name=exp_name, exp_note=exp_note):
                tmp = st.Stage(name, note) if note else st.Stage(name)
                self.assertIsInstance(tmp, st.Stage)
                self.assertEqual(tmp.name, exp_name)
                self.assertEqual(tmp.note, exp_note)

    def test_move(self):
        data = [
                (("test", "apple"),
                    (inf.Info("test"), inf.Info("apple"))),
                ]

        for v, expected in data:
            with self.subTest(v=v, expected=expected):
                tmp = self.bus.move(*v)
                self.assertIsInstance(tmp, st.sb.act.Action)
                self.assertEqual(tmp.act_type, em.ActType.MOVE)
                self.assertEqual(tmp.subject, self.bus)
                self.assertEqual(tmp.verb, "move")
                self.assertEqual(tmp.objects, expected)


