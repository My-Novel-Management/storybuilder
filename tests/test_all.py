# -*- coding: utf-8 -*-
"""Test suite for all tests
"""
## official library
import unittest
## local files
import test_action
import test_analyzer
import test_assertion
import test_baseactor
import test_basecontainer
import test_basedata
import test_block
import test_buildtool
import test_chapter
import test_checker
import test_converter
import test_counter
import test_datapack
import test_day
import test_drawer
import test_episode
import test_extractor
import test_item
import test_layer
import test_parser
import test_person
import test_rubi
import test_scene
import test_shot
import test_stage
import test_story
import test_time
import test_util_compare
import test_util_str
import test_util_tools
import test_when
import test_where
import test_who
import test_word
import test_world
import test_writer


def suite():
    '''Packing all tests.
    '''
    suite = unittest.TestSuite()

    suite.addTests((
        ## utility
        unittest.makeSuite(test_analyzer.AnalyzerTest),
        unittest.makeSuite(test_assertion.MethodsTest),
        unittest.makeSuite(test_util_compare.MethodsTest),
        unittest.makeSuite(test_util_str.MethodsTest),
        unittest.makeSuite(test_util_tools.MethodsTest),
        ## data
        unittest.makeSuite(test_basedata.BaseDataTest),
        unittest.makeSuite(test_datapack.DataPackTest),
        unittest.makeSuite(test_day.DayTest),
        unittest.makeSuite(test_item.ItemTest),
        unittest.makeSuite(test_layer.LayerTest),
        unittest.makeSuite(test_person.PersonTest),
        unittest.makeSuite(test_rubi.RubiTest),
        unittest.makeSuite(test_shot.ShotTest),
        unittest.makeSuite(test_stage.StageTest),
        unittest.makeSuite(test_time.TimeTest),
        unittest.makeSuite(test_when.WhenTest),
        unittest.makeSuite(test_where.WhereTest),
        unittest.makeSuite(test_who.WhoTest),
        unittest.makeSuite(test_word.WordTest),
        ## container
        unittest.makeSuite(test_basecontainer.BaseContainerTest),
        unittest.makeSuite(test_action.ActionTest),
        unittest.makeSuite(test_block.BlockTest),
        unittest.makeSuite(test_chapter.ChapterTest),
        unittest.makeSuite(test_episode.EpisodeTest),
        unittest.makeSuite(test_scene.SceneTest),
        unittest.makeSuite(test_story.StoryTest),
        ## actor
        unittest.makeSuite(test_baseactor.BaseActorTest),
        unittest.makeSuite(test_drawer.DrawerTest),
        unittest.makeSuite(test_writer.WriterTest),
        ## tools
        unittest.makeSuite(test_buildtool.BuildTest),
        unittest.makeSuite(test_checker.CheckerTest),
        unittest.makeSuite(test_converter.ConverterTest),
        unittest.makeSuite(test_counter.CounterTest),
        unittest.makeSuite(test_extractor.ExtractorTest),
        unittest.makeSuite(test_parser.ParserTest),
        ## main
        unittest.makeSuite(test_world.WorldTest),
        ))

    return suite

