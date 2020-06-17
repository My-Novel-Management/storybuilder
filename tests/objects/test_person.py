# -*- coding: utf-8 -*-
'''
Person class test
===============
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.objects import person as psn


class PersonTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(psn.__name__, 'Person class')

    def test_instance(self):
        data = [
                # (name, fullname, age, birth, sex, job, calling, info,
                #   exp_name, exp_age, exp_birth, exp_sex, exp_job, exp_calling, exp_info,
                #   exp_firstname, exp_lastname, exp_fullname, exp_exfullname)
                (True, 'Taro', '', 17, (5,5), 'male', 'student', 'me:俺', 'a man',
                    'Taro', 17, (5,5), 'male', 'student', {'me':'俺','S':'Taro','M':'俺'}, 'a man',
                    'Taro', 'Taro', 'Taro', 'Taro'),
                ]
        def checker(name, fullname, age, birth, sex, job, calling, info, exp_name,
                exp_age, exp_birth, exp_sex, exp_job, exp_calling, exp_info, exp_fn,
                exp_ln, exp_full, exp_exfull):
            tmp = psn.Person(name, fullname, age, birth, sex, job, calling, info)
            self.assertIsInstance(tmp, psn.Person)
            self.assertEqual(tmp.name, exp_name)
            self.assertEqual(tmp.age, exp_age)
            self.assertEqual(tmp.birth, exp_birth)
            self.assertEqual(tmp.sex, exp_sex)
            self.assertEqual(tmp.job, exp_job)
            self.assertEqual(tmp.calling, exp_calling)
            self.assertEqual(tmp.info, exp_info)
            self.assertEqual(tmp.firstname, exp_fn)
            self.assertEqual(tmp.lastname, exp_ln)
            self.assertEqual(tmp.fullname, exp_full)
            self.assertEqual(tmp.exfullname, exp_exfull)
        validate_with_fail(self, 'class instance', checker, data)

