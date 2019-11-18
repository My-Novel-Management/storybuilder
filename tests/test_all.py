# -*- coding: utf-8 -*-
"""Test suite for all tests
"""
## official library
import unittest
## local files
import test_action
import test_analyzer
import test_assertion
import test_basecontainer
import test_basedata
import test_basesubject
import test_buildtool
import test_chapter
import test_chara
import test_combaction
import test_day
import test_description
import test_episode
import test_extractor
import test_flag
import test_formatter
import test_it
import test_item
import test_parser
import test_person
import test_scene
import test_stage
import test_story
import test_strutils
import test_time
import test_utils
import test_who
import test_word
import test_world


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
        unittest.makeSuite(test_extractor.ExtractorTest),
        unittest.makeSuite(test_formatter.FormatterTest),
        unittest.makeSuite(test_strutils.MethodsTest),
        unittest.makeSuite(test_utils.MethodsTest),
        # data type
        unittest.makeSuite(test_chara.CharaTest),
        unittest.makeSuite(test_day.DayTest),
        unittest.makeSuite(test_flag.FlagTest),
        unittest.makeSuite(test_flag.NoFlagTest),
        unittest.makeSuite(test_flag.NoDeflagTest),
        unittest.makeSuite(test_it.ItTest),
        unittest.makeSuite(test_item.ItemTest),
        unittest.makeSuite(test_person.PersonTest),
        unittest.makeSuite(test_stage.StageTest),
        unittest.makeSuite(test_time.TimeTest),
        unittest.makeSuite(test_who.WhoTest),
        unittest.makeSuite(test_who.WhenTest),
        unittest.makeSuite(test_who.WhereTest),
        unittest.makeSuite(test_word.WordTest),
        # container type
        unittest.makeSuite(test_action.ActionTest),
        unittest.makeSuite(test_action.TagActionTest),
        unittest.makeSuite(test_chapter.ChapterTest),
        unittest.makeSuite(test_combaction.CombActionTest),
        unittest.makeSuite(test_description.DescriptionTest),
        unittest.makeSuite(test_description.NoDescTest),
        unittest.makeSuite(test_episode.EpisodeTest),
        unittest.makeSuite(test_scene.SceneTest),
        unittest.makeSuite(test_story.StoryTest),
        # world
        unittest.makeSuite(test_world.UtilityDictTest),
        unittest.makeSuite(test_world.WorldTest),
        # tools
        unittest.makeSuite(test_analyzer.AnalyzerTest),
        unittest.makeSuite(test_buildtool.BuildTest),
        unittest.makeSuite(test_parser.ParserTest),
        ))

    return suite

