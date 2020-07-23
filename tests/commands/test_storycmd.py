# -*- coding: utf-8 -*-
'''
StoryCmd class test
===================
'''

import argparse
import unittest
from tests.testutils import print_testtitle, validate_with_fail
from builder.commands import storycmd as cmd
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.datatypes.database import Database


class StoryCmdTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_testtitle(cmd.__name__, 'StoryCmd class')

    def test_instance(self):
        tmp = cmd.StoryCmd(Database())
        self.assertIsInstance(tmp, cmd.StoryCmd)

    #
    # for Container
    #

    def test_chapter(self):
        scmd = cmd.StoryCmd(Database())
        data = [
                # (title, args, outline, expect)
                (True, 'test', ('a','b'), 'apple', 'test'),
                ]
        def checker(title, args, outline, expect):
            tmp = scmd.chapter(title, *args, outline=outline)
            self.assertIsInstance(tmp, Chapter)
            self.assertEqual(tmp.title, expect)
        validate_with_fail(self, 'chapter', checker, data)

    def test_episode(self):
        scmd = cmd.StoryCmd(Database())
        data = [
                # (title, args, outline, expect)
                (True, 'test', ('a','b'), 'apple', 'test'),
                ]
        def checker(title, args, outline, expect):
            tmp = scmd.episode(title, *args, outline=outline)
            self.assertIsInstance(tmp, Episode)
            self.assertEqual(tmp.title, expect)
        validate_with_fail(self, 'episode', checker, data)

    def test_scene(self):
        scmd = cmd.StoryCmd(Database())
        data = [
                # (title, args, outline, expect)
                (True, 'test', ('a', 'b'), 'apple', 'test'),
                ]
        def checker(title, args, outline, expect):
            tmp = scmd.scene(title, *args, outline=outline)
            self.assertIsInstance(tmp, Scene)
            self.assertEqual(tmp.title, expect)
        validate_with_fail(self, 'scene', checker, data)

    #
    # for Scene control
    #

    def test_change_camera(self):
        db = Database()
        db.append_person('taro', '太郎','', 15,(1,1), 'm', 'student')
        scmd = cmd.StoryCmd(db)
        data = [
                # (key, expect)
                (True, 'taro', '太郎'),
                ]
        def checker(key, expect):
            tmp = scmd.change_camera(key)
            self.assertIsInstance(tmp, SCode)
            self.assertEqual(tmp.cmd, SCmd.CHANGE_CAMEARA)
            self.assertEqual(tmp.src.name, expect)
        validate_with_fail(self, 'change_camera', checker, data)

    def test_change_stage(self):
        db = Database()
        db.append_stage('room', '部屋')
        scmd = cmd.StoryCmd(db)
        data = [
                # (key, expect)
                (True, 'room', '部屋'),
                ]
        def checker(key, expect):
            tmp = scmd.change_stage(key)
            self.assertIsInstance(tmp, SCode)
            self.assertEqual(tmp.cmd, SCmd.CHANGE_STAGE)
            self.assertEqual(tmp.src.name, expect)
        validate_with_fail(self, 'change_stage', checker, data)

    def test_change_day(self):
        import datetime
        db = Database()
        db.append_day('d1', 'day1', 1,1,2020)
        scmd = cmd.StoryCmd(db)
        data = [
                # (keys, expect, exp_date)
                (True, ('d1',), 'day1', datetime.date(2020,1,1)),
                (True, (2,2,1000), '', datetime.date(1000,2,2)),
                ]
        def checker(keys, expect, exp_date):
            tmp = scmd.change_date(*keys)
            self.assertIsInstance(tmp, SCode)
            self.assertEqual(tmp.cmd, SCmd.CHANGE_DATE)
            self.assertEqual(tmp.src.name, expect)
            self.assertEqual(tmp.src.date, exp_date)
        validate_with_fail(self, 'change_date', checker, data)

    def test_change_time(self):
        import datetime
        db = Database()
        db.append_time('t1', 'noon', 12,00)
        scmd = cmd.StoryCmd(db)
        data = [
                # (keys, expect, exp_time)
                (True, ('t1',), 'noon', datetime.time(12,00)),
                (True, (11,00), '', datetime.time(11,00)),
                ]
        def checker(keys, expect, exp_time):
            tmp = scmd.change_time(*keys)
            self.assertIsInstance(tmp, SCode)
            self.assertEqual(tmp.cmd, SCmd.CHANGE_TIME)
            self.assertEqual(tmp.src.name, expect)
            self.assertEqual(tmp.src.time, exp_time)
        validate_with_fail(self, 'change_time', checker, data)
