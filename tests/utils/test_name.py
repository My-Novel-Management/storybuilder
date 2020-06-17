# -*- coding: utf-8 -*-
'''
Naming utility methods test
===========================
'''

import unittest
from testutils import print_testtitle, validate_with_fail
from builder.utils import util_name as uname


class MethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(uname.__name__, 'naming-utility methods')

    def test_name_set_from(self):
        data = [
                # (base, name, expect)
                (True, '田中,太郎', '太郎', ('太郎','田中', '田中太郎', '太郎・田中')),
                ]
        validate_with_fail(self, 'name_set_from',
                lambda base, name, expect: self.assertEqual(
                    uname.name_set_from(base, name), expect),
                data)

