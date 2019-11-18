# -*- coding: utf-8 -*-
"""Test: prson.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.person import Person


_FILENAME = "person.py"


class PersonTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "Person class")

    def test_attributes(self):
        data = [
                (False, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", "学生", "me:俺", "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (False, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", "学生", "me:俺", None,
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, Person.__NOTE__,),
                (False, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", "学生", None, None,
                    "山田太郎", {"me":"私","S":"太郎","M":"私"}, Person.__NOTE__,),
                (True, 1, "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", "学生", "me:俺", "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (True, "太郎", "山田", "太郎", 1, "山田・太郎",
                    17, "male", "学生", "me:俺", "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (True, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    "17", "male", "学生", "me:俺", "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (True, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, 1, "学生", "me:俺", "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (True, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", 1, "me:俺", "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (True, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", "学生", 1, "a man",
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                (True, "太郎", "山田", "太郎", "山田,太郎", "山田・太郎",
                    17, "male", "学生", "me:俺", 1,
                    "山田太郎", {"me":"俺","S":"太郎","M":"俺"}, "a man",),
                ]
        def _create(name, fullname, age, sex, job, calling, note):
            if note:
                return Person(name, fullname, age, sex, job, calling, note)
            elif calling:
                return Person(name, fullname, age, sex, job, calling)
            else:
                return Person(name, fullname, age, sex, job)
        def _checkcode(name, lastname, firstname, fullname1, exfullname,
                age, sex, job, calling1, note1,
                fullname2, calling2, note2):
            tmp = _create(name, fullname1, age, sex, job, calling1, note1)
            self.assertIsInstance(tmp, Person)
            self.assertEqual(tmp.name, name)
            self.assertEqual(tmp.lastname, lastname)
            self.assertEqual(tmp.firstname, firstname)
            self.assertEqual(tmp.fullname, fullname2)
            self.assertEqual(tmp.exfullname, exfullname)
            self.assertEqual(tmp.age, age)
            self.assertEqual(tmp.sex, sex)
            self.assertEqual(tmp.job, job)
            self.assertEqual(tmp.calling, calling2)
            self.assertEqual(tmp.note, note2)
        validated_testing_withfail(self, "attributes", _checkcode, data)

    def test_inherited(self):
        base_name, base_fullname = "太郎", "山田,太郎"
        base_age, base_sex, base_job = 17, "male", "学生"
        base_calling, base_note = "me:俺", "a man"
        data = [
                (False, "花子", "田中", "花子", "田中,花子", "田中・花子",
                    16, "female", "高校生", "me:私", "a girl",
                    "田中花子", {"me":"私","S":"花子","M":"私"}, "a girl",),
                (True, 1, "田中", "花子", "田中,花子", "田中・花子",
                    16, "female", "高校生", "me:私", "a girl",
                    "田中花子", {"me":"私","S":"花子","M":"私"}, "a girl",),
                ]
        def _create(person: Person, name, fullname, age, sex, job, calling, note):
            if note:
                return person.inherited(name, fullname, age, sex, job, calling, note)
            elif calling:
                return person.inherited(name, fullname, age, sex, job, calling)
            else:
                return person.inherited(name, fullname, age, sex, job)
        def _checkcode(name, lastname, firstname, fullname1, exfullname,
                    age, sex, job, calling1, note1,
                    fullname2, calling2, note2):
            tmp = Person(base_name, base_fullname, base_age, base_sex, base_job,
                    base_calling, base_note)
            tmp1 = _create(tmp, name, fullname1, age, sex, job, calling1, note1)
            self.assertIsInstance(tmp1, Person)
            self.assertEqual(tmp1.name, name)
            self.assertEqual(tmp1.lastname, lastname)
            self.assertEqual(tmp1.firstname, firstname)
            self.assertEqual(tmp1.fullname, fullname2)
            self.assertEqual(tmp1.exfullname, exfullname)
            self.assertEqual(tmp1.age, age)
            self.assertEqual(tmp1.sex, sex)
            self.assertEqual(tmp1.job, job)
            self.assertEqual(tmp1.calling, calling2)
            self.assertEqual(tmp1.note, note2)
        validated_testing_withfail(self, "inherited", _checkcode, data)
