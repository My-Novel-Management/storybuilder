# -*- coding: utf-8 -*-
"""Test suite for all tests
"""
import unittest
import test_assertion
import test_basecontainer
import test_basedata
import test_world
import test_chapter
import test_scene
import test_stage
import test_day
import test_time
import test_person
import test_action
import test_description


def suite():
    '''Packing all tests.
    '''
    suite = unittest.TestSuite()

    suite.addTests((
        # base type
        unittest.makeSuite(test_basecontainer.BaseContainerTest),
        unittest.makeSuite(test_basedata.BaseDataTest),
        unittest.makeSuite(test_basedata.NoDataTest),
        # utility
        unittest.makeSuite(test_assertion.MethodsTest),
        # data type
        ## stage
        unittest.makeSuite(test_stage.StageTest),
        ## day
        unittest.makeSuite(test_day.DayTest),
        ## time
        unittest.makeSuite(test_time.TimeTest),
        ## person
        unittest.makeSuite(test_person.PersonTest),
        ## action
        unittest.makeSuite(test_action.ActionTest),
        ## description
        unittest.makeSuite(test_description.DescriptionTest),
        # container type
        ## chapter
        unittest.makeSuite(test_chapter.ChapterTest),
        unittest.makeSuite(test_scene.SceneTest),
        # world
        unittest.makeSuite(test_world.UtilityDictTest),
        unittest.makeSuite(test_world.WorldTest),
        ))

    return suite

