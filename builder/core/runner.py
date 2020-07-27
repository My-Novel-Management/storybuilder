# -*- coding: utf-8 -*-
'''
Runner Object
=============
'''

from __future__ import annotations

__all__ = ('Runner',)


from analyzer.analyzer import Analyzer
from builder.commands.optioncmd import OptionParser
from builder.containers.story import Story
from builder.core.commentconverter import CommentConverter
from builder.core.compiler import Compiler
from builder.core.executer import Executer
from builder.core.filter import Filter
from builder.core.formatter import Formatter
from builder.core.headerupdater import HeaderUpdater
from builder.core.outputter import Outputter
from builder.core.plotupdater import PlotUpdater
from builder.core.reducer import Reducer
from builder.core.sceneupdater import SceneUpdater
from builder.core.serializer import Serializer
from builder.core.tagreplacer import TagReplacer
from builder.core.validater import Validater
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.compilemode import CompileMode
from builder.datatypes.database import Database
from builder.datatypes.formatmode import FormatMode
from builder.datatypes.outputmode import OutputMode
from builder.datatypes.rawdata import RawData
from builder.datatypes.resultdata import ResultData
from builder.datatypes.storyconfig import StoryConfig
from builder.datatypes.textlist import TextList
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
        self._is_analyzed = assertion.is_bool(False)
        self._is_debug = assertion.is_bool(False)

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
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Finish: Pre-Compile')

        LOG.info('RUN: START-PHASE: Compile and Output')
        result = assertion.is_instance(self._compile(tmp, config, db), ResultData)
        LOG.info('... SUCCESS: Finish: Compile and Output')

        self._output_storyinfo(config)

        LOG.info('RUN: analyzer check')
        if self._is_analyzed:
            result = assertion.is_instance(self._analyze_and_output(tmp, db.get_person_names(),
                self._is_debug),
                    ResultData)

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
            LOG.debug(f'RUN: option rubi: {opts.rubi}')
            config.set_is_rubi(True)

        if opts.comment:
            LOG.debug(f'RUN: option comment: {opts.comment}')
            config.set_is_comment(True)

        if opts.console:
            LOG.debug(f'RUN: option console: {opts.console}')
            config.set_output_mode(OutputMode.CONSOLE)

        if opts.format:
            LOG.debug(f'RUN: option format: {opts.format}')
            config.set_format_mode(FormatMode.conv_to_mode(opts.format))

        if opts.part:
            LOG.debug(f'RUN: option part: {opts.part}')
            start, end = 0, -1
            if ':' in opts.part:
                _ = opts.part.split(':')
                start, end = int(_[0]), int(_[1])
            else:
                start = end = int(opts.part)
            config.set_start(start)
            config.set_end(end)

        if opts.data:
            LOG.debug(f'RUN: option data: {opts.data}')
            config.set_is_data(opts.data)

        if opts.plot:
            LOG.debug(f'RUN: option plot: {opts.plot}')
            config.set_is_plot(opts.plot)

        if opts.priority:
            LOG.debug(f'RUN: option priority: {opts.priority}')
            config.set_priority(opts.priority)

        if opts.text:
            LOG.debug(f'RUN: option text: {opts.text}')
            config.set_is_text(opts.text)

        if opts.analyze:
            LOG.debug(f'RUN: option analyze: {opts.analyze}')
            self._is_analyzed = True

        if opts.debug:
            LOG.debug(f'RUN: option debug: {opts.debug}')
            self._is_debug = True

        return is_succeeded

    def _pre_compile(self, src: Story, config: StoryConfig, db: Database) -> ResultData:
        LOG.info('RUN: START: Comment Converter')
        result = assertion.is_instance(CommentConverter().execute(src), ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in CommentConverter!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: CommentConverter')

        LOG.info('RUN: START: Filter')
        result = assertion.is_instance(Filter().execute(tmp, config.priority),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in Filter!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Filter')

        LOG.info('RUN: START: Reducer')
        result = assertion.is_instance(Reducer().execute(tmp, config),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in Reducer!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Reducer')

        LOG.info('RUN: START: Replacer')
        result = assertion.is_instance(TagReplacer().execute(tmp, config, db.tags),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in TagReplacer!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: Replacer')

        LOG.info('RUN: START: header updater')
        result = assertion.is_instance(HeaderUpdater().execute(tmp, config),
                ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in HeaderUpdater!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: HeaderUpdater')

        LOG.info('RUN: START: scene updater')
        result = assertion.is_instance(SceneUpdater().execute(tmp), ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in SceneUpdater!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: SceneUpdater')

        LOG.info('RUN: START: plot updater')
        result = assertion.is_instance(PlotUpdater().execute(tmp), ResultData)
        if not result.is_succeeded:
            LOG.error('Failure in PlotUpdater!!')
            return result
        tmp = assertion.is_instance(result.data, Story)
        LOG.info('... SUCCESS: PlotUpdater')

        return result

    def _compile(self, src: Story, config: StoryConfig, db: Database) -> ResultData:
        assertion.is_instance(src, Story)
        assertion.is_instance(config, StoryConfig)
        assertion.is_instance(db, Database)

        cmp_flags = assertion.is_valid_length(
                        [True, config.is_plot, config.is_text,
                        config.is_data,
                        config.is_scenario, config.is_audiodrama],
                        len(CompileMode.get_all()))
        cmp_modes = assertion.is_valid_length(
                        [CompileMode.NORMAL, CompileMode.PLOT, CompileMode.NOVEL_TEXT,
                        CompileMode.STORY_DATA,
                        CompileMode.SCENARIO, CompileMode.AUDIODRAMA],
                        len(CompileMode.get_all()))

        slz_idx = 0
        cmp_src_list = [None] * len(CompileMode.get_all())

        for flag in cmp_flags:
            if flag:
                LOG.info(f'RUN: START: Serializer and Validater [{slz_idx}]')
                result = assertion.is_instance(Serializer().execute(src, cmp_modes[slz_idx]),
                            ResultData)
                if not result.is_succeeded:
                    LOG.error('Failure in Serializer!!')
                    return result
                tmp = assertion.is_instance(result.data, CodeList)
                LOG.info(f'... SUCCESS: Serializer [{slz_idx}]')

                result = assertion.is_instance(Validater().execute(tmp), ResultData)
                if not result.is_succeeded:
                    LOG.error('Failure in Validater')
                    return result
                LOG.info(f'... SUCCESS: Validater [{slz_idx}]')
                cmp_src_list[slz_idx] = assertion.is_instance(result.data, CodeList)
            slz_idx += 1

        cmp_idx = 0
        cmp_data_list = [None] * len(CompileMode.get_all())
        compiler = Compiler()

        for flag in cmp_flags:
            if flag:
                LOG.info(f'RUN: START: Compiler [{cmp_idx}]')
                result = assertion.is_instance(
                        compiler.execute(cmp_src_list[cmp_idx], cmp_modes[cmp_idx],
                            db.rubis, config.is_rubi, config.is_comment),
                        ResultData)
                if not result.is_succeeded:
                    LOG.error(f'Failure in Compiler [{cmp_idx}]!!')
                    return result
                cmp_data_list[cmp_idx] = assertion.is_instance(result.data, RawData)
                LOG.info(f'... SUCCESS Compiler [{cmp_idx}]')
            cmp_idx += 1

        LOG.info('<UNIMP> RUN: START-PHASE: Format')

        fmt_idx = 0
        fmt_data_list = [None] * len(CompileMode.get_all())
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
                fmt_data_list[fmt_idx] = assertion.is_instance(result.data, TextList)
                LOG.info(f'... SUCCESS Formatter [{fmt_idx}]')
            fmt_idx += 1

        return self._output(fmt_data_list, config)

    def _output(self, src: list, config: StoryConfig) -> ResultData:
        LOG.info('RUN: OUTPUT: start')
        assertion.is_instance(config, StoryConfig)

        result = ResultData(src, True, None)
        prefixs = assertion.is_valid_length(['', '_p', '', '_data', '_sc', '_ad'],
                    len(CompileMode.get_all()))
        extentions = assertion.is_valid_length(['md', 'md', 'txt', 'md', 'md', 'md'],
                    len(CompileMode.get_all()))
        fmt_idx = 0
        outputter = Outputter()

        for fmt_data in assertion.is_listlike(src):
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
            fmt_idx += 1

        return result


    def _output_storyinfo(self, config: StoryConfig) -> None:
        version = config.version
        chars = config.desc_size
        papers = config.desc_papers
        totals = config.total_size
        t_papers = config.total_papers
        print(f'>> v{version} / {papers}p({chars}c) / {t_papers}p({totals}c)')


    def _analyze_and_output(self, src: Story, person_names: list, is_debug: bool) -> ResultData:
        # serialize and compile as text
        mode = CompileMode.NOVEL_TEXT
        fmode = FormatMode.DEFAULT
        LOG.info('Serialize for Analyzer')
        result = assertion.is_instance(Serializer().execute(src, mode), ResultData)
        if not result.is_succeeded:
            return result
        tmp = assertion.is_instance(result.data, CodeList)
        LOG.info('Validate for Analyzer')
        result = assertion.is_instance(Validater().execute(tmp), ResultData)
        if not result.is_succeeded:
            return result
        tmp = assertion.is_instance(result.data, CodeList)
        LOG.info('Compile for Analyzer')
        result = assertion.is_instance(Compiler().execute(tmp, mode, {}, False, False),
                ResultData)
        if not result.is_succeeded:
            return result
        tmp = assertion.is_instance(result.data, RawData)
        LOG.info('Format for Analyzer')
        result = assertion.is_instance(Formatter().execute(tmp, fmode), ResultData)
        if not result.is_succeeded:
            return result
        tmp = assertion.is_instance(result.data, TextList)

        LOG.info('RUN: call Analyzer')
        result = Analyzer().execute(tmp, person_names, is_debug)
        return ResultData([], True, None)

