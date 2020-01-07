# -*- coding: utf-8 -*-
"""Test suite for all tests
"""
## official library
import unittest
## local libs
import test_utildict
import test_utils_assertion
import test_utils_id
import test_utils_math
import test_utils_str
## local files
import test_action
import test_analyzer
import test_basecontainer
import test_basedata
import test_block
import test_buildtool
import test_chapter
import test_converter
import test_counter
import test_day
import test_episode
import test_extractor
import test_formatter
import test_item
import test_layer
import test_metadata
import test_parser
import test_person
import test_pronoun
import test_rubi
import test_scene
import test_stage
import test_story
import test_time
import test_utility
import test_word
import test_world
import test_writer


def suite():
    '''Packing all tests.
    '''
    suite = unittest.TestSuite()

    suite.addTests((
        ## utility
        unittest.makeSuite(test_utildict.UtilityDictTest),
        unittest.makeSuite(test_utils_assertion.MethodsTest),
        unittest.makeSuite(test_utils_id.MethodsTest),
        unittest.makeSuite(test_utils_math.MethodsTest),
        unittest.makeSuite(test_utils_str.MethodsTest),
        unittest.makeSuite(test_utility.MethodsTest),
        ## data
        unittest.makeSuite(test_basedata.BaseDataTest),# base
        unittest.makeSuite(test_day.DayTest),
        unittest.makeSuite(test_item.ItemTest),
        unittest.makeSuite(test_metadata.MetaDataTest),
        unittest.makeSuite(test_person.PersonTest),
        unittest.makeSuite(test_stage.StageTest),
        unittest.makeSuite(test_time.TimeTest),
        unittest.makeSuite(test_word.WordTest),
        unittest.makeSuite(test_pronoun.PronounClassesTest),
        unittest.makeSuite(test_rubi.RubiTest),
        unittest.makeSuite(test_layer.LayerTest),
        ## container
        unittest.makeSuite(test_basecontainer.BaseContainerTest),# base
        unittest.makeSuite(test_action.ActionTest),
        unittest.makeSuite(test_block.BlockTest),
        unittest.makeSuite(test_scene.SceneTest),
        unittest.makeSuite(test_episode.EpisodeTest),
        unittest.makeSuite(test_chapter.ChapterTest),
        unittest.makeSuite(test_story.StoryTest),
        ## actor
        ## tools
        unittest.makeSuite(test_analyzer.AnalyzerTest),
        unittest.makeSuite(test_buildtool.BuildTest),
        unittest.makeSuite(test_converter.ConverterTest),
        unittest.makeSuite(test_counter.CounterTest),
        unittest.makeSuite(test_extractor.ExtractorTest),
        unittest.makeSuite(test_formatter.FormatterTest),
        unittest.makeSuite(test_parser.ParserTest),
        unittest.makeSuite(test_writer.WriterTest),
        ## main
        unittest.makeSuite(test_world.WorldTest),
        ))

    return suite

