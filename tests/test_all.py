# -*- coding: utf-8 -*-
"""Test suite for all tests
"""
import unittest
import test_assertion
import test_basecontainer
import test_basedata
import test_basesubject
import test_chara
import test_episode
import test_it
import test_item
import test_story
import test_strutils
import test_world
import test_chapter
import test_scene
import test_stage
import test_day
import test_time
import test_person
import test_action
import test_description
import test_combaction
import test_flag


def suite():
    '''Packing all tests.
    '''
    suite = unittest.TestSuite()

    suite.addTests((
        # base type
        unittest.makeSuite(test_basecontainer.BaseContainerTest),
        unittest.makeSuite(test_basedata.BaseDataTest),
        unittest.makeSuite(test_basedata.NoDataTest),
        unittest.makeSuite(test_basesubject.BaseSubjectTest),
        unittest.makeSuite(test_basesubject.NoSubjectTest),
        # utility
        unittest.makeSuite(test_assertion.MethodsTest),
        unittest.makeSuite(test_strutils.MethodsTest),
        # data type
        unittest.makeSuite(test_flag.FlagTest),
        unittest.makeSuite(test_flag.NoFlagTest),
        unittest.makeSuite(test_flag.NoDeflagTest),
        unittest.makeSuite(test_it.ItTest),
        unittest.makeSuite(test_item.ItemTest),
        unittest.makeSuite(test_story.StoryTest),
        ## stage
        unittest.makeSuite(test_stage.StageTest),
        ## day
        unittest.makeSuite(test_day.DayTest),
        ## time
        unittest.makeSuite(test_time.TimeTest),
        ## person
        unittest.makeSuite(test_person.PersonTest),
        unittest.makeSuite(test_chara.CharaTest),
        ## action
        unittest.makeSuite(test_action.ActionTest),
        ## description
        unittest.makeSuite(test_description.DescriptionTest),
        unittest.makeSuite(test_description.NoDescTest),
        # container type
        ## chapter
        unittest.makeSuite(test_chapter.ChapterTest),
        unittest.makeSuite(test_episode.EpisodeTest),
        unittest.makeSuite(test_scene.SceneTest),
        # world
        unittest.makeSuite(test_world.UtilityDictTest),
        unittest.makeSuite(test_world.WorldTest),
        ## container
        unittest.makeSuite(test_combaction.CombActionTest),
        ))

    return suite

