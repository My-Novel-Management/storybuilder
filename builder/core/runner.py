# -*- coding: utf-8 -*-
'''
Runner Object
=============
'''

from __future__ import annotations

__all__ = ('Runner',)


from builder.commands.optioncmd import OptionParser
from builder.containers.story import Story
from builder.core.compiler import Compiler, CompileMode
from builder.core.executer import Executer
from builder.core.filter import Filter
from builder.core.formatter import Formatter
from builder.core.headerupdater import HeaderUpdater
from builder.core.outputter import Outputter
from builder.core.reducer import Reducer
from builder.core.serializer import Serializer
from builder.core.tagreplacer import TagReplacer
from builder.core.validater import Validater
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.database import Database
from builder.datatypes.formatmode import FormatMode
from builder.datatypes.outputmode import OutputMode
from builder.datatypes.rawdata import RawData
from builder.datatypes.resultdata import ResultData
from builder.datatypes.storyconfig import StoryConfig
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class RunnerError(BuilderError):
    ''' General Error in Runner.
    '''
    pass


class Runner(Executer):
    ''' Runner class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('RUNNER: initialize')

    #
    # methods
    #

    def execute(self, src: Story,
            config: StoryConfig, db: Database,
            ) -> ResultData: # pragma: no cover
        ''' Exec story building, compiling and outputting.

        NOTE: Compile option
            1. normal: output `story.md`
            2. plot: output `plot.md`
            3. text: output `story.txt`
            4. scenario: output `sc_story.md`
        '''
        LOG.info('RUN: == START EXEC ==')
        LOG.info('RUN: START-PHASE: Preparation')

        tmp = assertion.is_instance(src, Story)
        is_succeeded = True
        result = None
        error = None

        is_succeeded = self._build_options(config)
        if not is_succeeded:
            msg = 'Cannot build option arguments!!'
            error = RunnerError(msg)
            LOG.error(msg)
            return ResultData([], is_succeeded, error)
        LOG.info('... SUCCESS: Preparation')

        LOG.info('RUN: START-PHASE: Pre-Compile')
        result = self._pre_compile(src, config, db)
        if not result.is_succeeded:
            return result
        tmp = assertion.is_instance(result.data, CodeList)
        LOG.info('... SUCCESS: Finish: Pre-Compile')

        LOG.info('RUN: START-PHASE: Compile and Output')
        result = assertion.is_instance(self._compile(tmp, config, db), ResultData)
        LOG.info('... SUCCESS: Finish: Compile and Output')

        LOG.info('RUN: == ALL SUCCEEDED ==')
        return result

    #
    # private methods
    #

    def _build_options(self, config :StoryConfig) -> bool: # pragma: no cover
        import argparse
        LOG.info('Call: build_options')
        opts = assertion.is_instance(OptionParser().get_commandline_arguments(),
                argparse.Namespace)
        LOG.debug(f'Get option arguments: {opts}')

        is_succeeded = True

        LOG.info('RUN: option settings')
        if opts.rubi:
            LOG.debug('RUN: option rubi: {opts.rubi}')
            config.set_is_rubi(True)

        if opts.debug:
            LOG.debug('RUN: option debug: {opts.debug}')
            config.set_output_mode(OutputMode.CONSOLE)

        if opts.comment:
            LOG.debug('RUN: option comment: {opts.comment}')
            config.set_is_comment(True)

        if opts.forcemecab:
            LOG.debug('<UNIMP>RUN: option forcemecab: {opts.forcemecab}')

        if opts.format:
            LOG.debug('<UNIMP>RUN: option format: {opts.format}')
            config.set_format_mode(FormatMode.conv_to_mode(opts.format))

        if opts.priority:
            LOG.debug('RUN: option priority: {opts.priority}')
            config.set_priority(opts.priority)

        return is_succeeded

    def _pre_compile(self, src: Story, config: StoryConfig, db: Database) -> ResultData:
        LOG.info('RUN: START: Filter')
        result = assertion.is_instance(Filter().execute(src, config.priority),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in Filter!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Filter')

        LOG.info('RUN: START: Reducer')
        result = assertion.is_instance(Reducer().execute(tmp, config.start, config.end),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in Reducer!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Reducer')

        LOG.info('RUN: START: Replacer')
        result = assertion.is_instance(TagReplacer().execute(tmp, db.tags),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in TagReplacer!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Replacer')

        LOG.info('RUN: START: header updater')
        result = assertion.is_instance(HeaderUpdater().execute(tmp),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in HeaderUpdater!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: HeaderUpdater')

        LOG.info('RUN: START: Serializer')
        result = assertion.is_instance(Serializer().execute(tmp),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in Serializer!!')
            return result
        tmp = assertion.is_instance(result.data, CodeList)
        LOG.info('... SUCCESS: Serializer')

        LOG.info('RUN: START: Validater')
        result = assertion.is_instance(Validater().execute(tmp), ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in Validater')
            return result
        LOG.info('... SUCCESS: Validater')
        return result

    def _compile(self, src: CodeList, config: StoryConfig, db: Database) -> ResultData:
        assertion.is_instance(src, CodeList)
        assertion.is_instance(config, StoryConfig)
        assertion.is_instance(db, Database)

        cmp_idx = 0
        cmp_normal = []
        cmp_plot = []
        cmp_text = []
        cmp_scenario = []
        cmp_audiodrama = []
        cmp_data_list = [cmp_normal, cmp_plot, cmp_text, cmp_scenario, cmp_audiodrama]
        cmp_flags = [True, config.is_plot, config.is_text,
                config.is_scenario, config.is_audiodrama]
        cmp_modes = [CompileMode.NORMAL, CompileMode.PLOT, CompileMode.NOVEL_TEXT,
                CompileMode.SCENARIO, CompileMode.AUDIODRAMA]
        compiler = Compiler()

        for flag in cmp_flags:
            if flag:
                LOG.info(f'RUN: START: Compiler [{cmp_idx}]')
                result = assertion.is_instance(
                        compiler.execute(src, cmp_modes[cmp_idx],
                            db.rubis, config.is_rubi, config.is_comment),
                        ResultData)
                if not result.is_succeeded:
                    LOG.error(f'Failure in Compiler [{cmp_idx}]!!')
                    return result
                cmp_data_list[cmp_idx] = result.data
                LOG.info(f'... SUCCESS Compiler [{cmp_idx}]')
            cmp_idx += 1

        LOG.info('<UNIMP> RUN: START-PHASE: Format')

        fmt_idx = 0
        fmt_normal = []
        fmt_plot = []
        fmt_text = []
        fmt_scenario = []
        fmt_audiodrama = []
        fmt_data_list = [fmt_normal, fmt_plot, fmt_text, fmt_scenario, fmt_audiodrama]
        formatter = Formatter()

        for cmp_data in cmp_data_list:
            if cmp_data:
                LOG.info(f'RUN: START: Formatter [{fmt_idx}]')
                result = assertion.is_instance(
                        formatter.execute(cmp_data, config.format_mode),
                        ResultData)
                if not result.is_succeeded:
                    LOG.error(f'Failure in Formatter [{fmt_idx}]!!')
                    return result
                fmt_data_list[fmt_idx] = result.data
                LOG.info(f'... SUCCESS Formatter [{fmt_idx}]')
            fmt_idx += 1

        return self._output(fmt_data_list, config)

    def _output(self, src: list, config: StoryConfig) -> ResultData:
        LOG.info('RUN: OUTPUT: start')
        assertion.is_instance(config, StoryConfig)

        result = ResultData(src, True, None)
        prefixs = ['', 'p', '', 'sc', 'ad']
        extentions = ['md', 'md', 'txt', 'md', 'md']
        fmt_idx = 0
        outputter = Outputter()

        for fmt_data in assertion.is_nearlylist(src):
            if fmt_data:
                LOG.info(f'RUN: START: Outputter [{fmt_idx}]')
                result = assertion.is_instance(
                    outputter.execute(fmt_data, config.output_mode,
                        config.filename, prefixs[fmt_idx], extentions[fmt_idx],
                        config.builddir),
                    ResultData)
                if not result.is_succeeded:
                    LOG.error(f'Failure in Outputter [{fmt_idx}]!!')
                    return result
                LOG.info(f'... SUCCESS: Outputter [{fmt_idx}]')

        return result

