# -*- coding: utf-8 -*-
'''
Stage class test
===============
'''

import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.objects import stage as st


class StageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(st.__name__, 'Stage class')

    def test_instance(self):
        data = [
                # (name, parent, geometry, info, expect, exp_p, exp_geo, exp_info)
                (True, 'test', 'on_Town', (5,5), 'a note', 'test', 'on_Town', (5,5), 'a note'),
                ]
        def checker(name, parent, geometry, info, expect, exp_p, exp_geo, exp_info):
            tmp = st.Stage(name, parent, geometry, info)
            self.assertIsInstance(tmp, st.Stage)
            self.assertEqual(tmp.name, expect)
            self.assertEqual(tmp.parent, exp_p)
            self.assertEqual(tmp.geometry, exp_geo)
            self.assertEqual(tmp.info, exp_info)
        validate_with_fail(self, 'class instance', checker, data)

