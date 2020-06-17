# -*- coding: utf-8 -*-
'''
Rubi class test
===============
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.objects import rubi as rb


class RubiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(rb.__name__, 'Rubi class')

    def test_instance(self):
        data = [
                # (name, rubi, exclusions, is_always, expect, exp_rubi, exp_excl, exp_al)
                (True, '太郎', '\\1《太郎》', (), True,
                    '太郎', '\\1《太郎》', (), True),
                ]
        def checker(name, rubi, exclusions, is_always, expect, exp_rubi, exp_excl, exp_al):
            tmp = rb.Rubi(name, rubi, exclusions, is_always)
            self.assertIsInstance(tmp, rb.Rubi)
            self.assertEqual(tmp.name, expect)
            self.assertEqual(tmp.rubi, exp_rubi)
            self.assertEqual(tmp.exclusions, exp_excl)
            self.assertEqual(tmp.is_always, exp_al)
        validate_with_fail(self, 'class instance', checker, data)

