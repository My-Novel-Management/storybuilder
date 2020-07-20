# -*- coding: utf-8 -*-
'''
The test suite for all test cases
=================================
'''
import unittest
from tests import test_world
from tests.commands import test_command
from tests.commands import test_optioncmd
from tests.commands import test_scode
from tests.commands import test_storycmd
from tests.commands import test_tagcmd
from tests.containers import test_container
from tests.core import test_compiler
from tests.core import test_filter
from tests.core import test_formatter
from tests.core import test_headerupdater
from tests.core import test_outputter
from tests.core import test_reducer
from tests.core import test_runner
from tests.core import test_serializer
from tests.core import test_tagreplacer
from tests.core import test_validater
from tests.datatypes import test_codelist
from tests.datatypes import test_compilemode
from tests.datatypes import test_database
from tests.datatypes import test_formatmode
from tests.datatypes import test_formattag
from tests.datatypes import test_headerinfo
from tests.datatypes import test_outputmode
from tests.datatypes import test_rawdata
from tests.datatypes import test_resultdata
from tests.datatypes import test_storyconfig
from tests.objects import test_day
from tests.objects import test_item
from tests.objects import test_person
from tests.objects import test_rubi
from tests.objects import test_sobject
from tests.objects import test_stage
from tests.objects import test_time
from tests.objects import test_word
from tests.objects import test_writer
from tests.tools import test_checker
from tests.tools import test_converter
from tests.tools import test_counter
from tests.utils import test_assertion
from tests.utils import test_dict
from tests.utils import test_list
from tests.utils import test_logger
from tests.utils import test_math
from tests.utils import test_name
from tests.utils import test_str


def suite() -> unittest.TestSuite:
    ''' Packing all tests.
    '''
    suite = unittest.TestSuite()

    suite.addTests((
        # commands
        unittest.makeSuite(test_command.SCmdEnumTest),
        unittest.makeSuite(test_optioncmd.OptionParserTest),
        unittest.makeSuite(test_scode.SCodeTest),
        unittest.makeSuite(test_storycmd.StoryCmdTest),
        unittest.makeSuite(test_tagcmd.TagCmdTest),
        # containers
        unittest.makeSuite(test_container.ContainerTest),
        # datatypes
        unittest.makeSuite(test_codelist.CodeListTest),
        unittest.makeSuite(test_compilemode.CompileModeTest),
        unittest.makeSuite(test_database.DatabaseTest),
        unittest.makeSuite(test_formatmode.FormatModeTest),
        unittest.makeSuite(test_formattag.FormatTagTest),
        unittest.makeSuite(test_headerinfo.HeaderInfoTest),
        unittest.makeSuite(test_outputmode.OutputModeTest),
        unittest.makeSuite(test_rawdata.RawDataTest),
        unittest.makeSuite(test_resultdata.ResultDataTest),
        unittest.makeSuite(test_storyconfig.StoryConfigTest),
        # objects
        unittest.makeSuite(test_day.DayTest),
        unittest.makeSuite(test_item.ItemTest),
        unittest.makeSuite(test_person.PersonTest),
        unittest.makeSuite(test_rubi.RubiTest),
        unittest.makeSuite(test_sobject.SObjectTest),
        unittest.makeSuite(test_stage.StageTest),
        unittest.makeSuite(test_time.TimeTest),
        unittest.makeSuite(test_word.WordTest),
        unittest.makeSuite(test_writer.WriterTest),
        # tools
        unittest.makeSuite(test_checker.CheckerTest),
        unittest.makeSuite(test_converter.ConverterTest),
        unittest.makeSuite(test_counter.CounterTest),
        # utility
        unittest.makeSuite(test_assertion.MethodsTest),
        unittest.makeSuite(test_dict.MethodsTest),
        unittest.makeSuite(test_list.MethodsTest),
        unittest.makeSuite(test_logger.MyLoggerTest),
        unittest.makeSuite(test_math.MethodsTest),
        unittest.makeSuite(test_name.MethodsTest),
        unittest.makeSuite(test_str.MethodsTest),
        # core
        unittest.makeSuite(test_compiler.CompilerTest),
        unittest.makeSuite(test_filter.FilterTest),
        unittest.makeSuite(test_formatter.FormatterTest),
        unittest.makeSuite(test_headerupdater.HeaderUpdaterTest),
        unittest.makeSuite(test_outputter.OutputterTest),
        unittest.makeSuite(test_reducer.ReducerTest),
        unittest.makeSuite(test_runner.RunnerTest),
        unittest.makeSuite(test_serializer.SerializerTest),
        unittest.makeSuite(test_tagreplacer.TagReplacerTest),
        unittest.makeSuite(test_validater.ValidaterTest),
        # main
        unittest.makeSuite(test_world.WorldTest),
        ))

    return suite

