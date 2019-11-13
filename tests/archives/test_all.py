# -*- coding: utf-8 -*-
"""Test suite for all tests
"""
import unittest
import test_action
import test_analyzer
import test_assertion
import test_baseaction
import test_basedescription
import test_basesubject
import test_buildtool
import test_day
import test_description
import test_info
import test_item
import test_parser
import test_person
import test_sobject
import test_stage
import test_strutils
import test_subject
import test_testutils
import test_world


def suite():
    '''Packing all tests.
    '''
    suite = unittest.TestSuite()

    suite.addTests((
        # base tools
        unittest.makeSuite(test_assertion.PublicMethodsTest),
        # base classes
        unittest.makeSuite(test_baseaction.BaseActionTest),
        unittest.makeSuite(test_basedescription.BaseDescTest),
        unittest.makeSuite(test_basesubject.BaseSubjectTest),
        unittest.makeSuite(test_sobject.SObjectTest),
        unittest.makeSuite(test_action.ActionTest),
        unittest.makeSuite(test_action.ActionGroupTest),
        unittest.makeSuite(test_action.TagActionTest),
        unittest.makeSuite(test_description.DescTest),
        unittest.makeSuite(test_description.DescGroupTest),
        # subject classes
        unittest.makeSuite(test_subject.SubjectTest),
        unittest.makeSuite(test_day.DayTest),
        unittest.makeSuite(test_info.InfoTest),
        unittest.makeSuite(test_info.FlagTest),
        unittest.makeSuite(test_info.DeflagTest),
        unittest.makeSuite(test_info.NothingTest),
        unittest.makeSuite(test_info.SomethingTest),
        unittest.makeSuite(test_item.ItemTest),
        unittest.makeSuite(test_person.PersonTest),
        unittest.makeSuite(test_stage.StageTest),
        # world
        unittest.makeSuite(test_world.AuxverbDictTest),
        unittest.makeSuite(test_world.SDictTest),
        unittest.makeSuite(test_world.TagManagerTest),
        unittest.makeSuite(test_world.WorldTest),
        # utility
        unittest.makeSuite(test_analyzer.PublicMethodsTest),
        unittest.makeSuite(test_parser.PublicMethodsTest),
        unittest.makeSuite(test_strutils.PublicMethodsTest),
        unittest.makeSuite(test_testutils.PublicMethodsTest),
        # build tool
        unittest.makeSuite(test_buildtool.PrivateMethodsTest),
        ))

    return suite

