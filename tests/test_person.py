# -*- coding: utf-8 -*-
"""Test: person.py
"""
## public libs
import unittest
## local files (test utils)
from testutils import printTestTitle, validatedTestingWithFail
## local files
from builder.person import Person


_FILENAME = "person.py"


class PersonTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        printTestTitle(_FILENAME, "Person class")

    def setUp(self):
        pass

    def test_attributes(self):
        attrs = ("fullname", "age", "sex", "job", "calling", "note")
        data = [
                (False, "Taro", "山田,太郎", 15, "male", "student", "me:俺", "a man",
                    ("山田,太郎", 15, "male", "student", {"me":"俺","S":"Taro","M":"俺"}, "a man")),
                ]
        def _creator(name, full, age, sex, job, calling, note):
            if calling and note:
                return Person(name, full, age, sex, job, calling, note)
            elif calling:
                return Person(name, full, age, sex, job, calling)
            elif note:
                return Person(name, full, age, sex, job, note=note)
            else:
                return Person(name, full, age, sex, job)
        def _checkcode(name, full, age, sex, job, calling, note, expects):
            tmp = _creator(name, full, age, sex, job, calling, note)
            self.assertIsInstance(tmp, Person)
            for a,v in zip(attrs, expects):
                with self.subTest(a=a, v=v):
                    self.assertEqual(getattr(tmp, a), v)
        validatedTestingWithFail(self, "class attributes", _checkcode, data)

