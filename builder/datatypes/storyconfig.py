# -*- coding: utf-8 -*-
'''
Story Config Object
===================
'''

from __future__ import annotations

__all__ = ('StoryConfig',)


import datetime
from builder import __PRIORITY_DEFAULT__, __PRIORITY_MAX__, __PRIORITY_MIN__
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.formatmode import FormatMode
from builder.datatypes.outputmode import OutputMode
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class StoryConfigError(BuilderError):
    ''' General StoryConfig Error.
    '''
    pass


class StoryConfig(object):
    ''' Config object class for a story building.
    '''

    def __init__(self, title: str):
        LOG.info('CONFIG: initialize')
        LOG.debug(f'-- title: {title}')
        # for story
        self._title = assertion.is_str(title)
        self._outline = assertion.is_str('__story_outline__')
        self._priority = assertion.is_int(__PRIORITY_DEFAULT__)
        self._start = assertion.is_int(0)
        self._end = assertion.is_int(-1)
        self._base_date = datetime.date(2020,1,1)
        self._base_time = datetime.time(12,00)
        self._version = assertion.is_tuple((1,0,0))
        self._columns = assertion.is_int(20)
        self._rows = assertion.is_int(20)
        # for compile
        self._is_plot = assertion.is_bool(False)
        self._is_text = assertion.is_bool(False)
        self._is_scenario = assertion.is_bool(False)
        self._is_audiodrama = assertion.is_bool(False)
        self._is_rubi = assertion.is_bool(False)
        self._is_comment = assertion.is_bool(False)
        self._is_console = assertion.is_bool(False)
        self._format_mode = assertion.is_instance(FormatMode.DEFAULT, FormatMode)
        self._output_mode = assertion.is_instance(OutputMode.FILE, OutputMode)
        self._filename = assertion.is_str('story')
        self._builddir = assertion.is_str('build')
        self._log_level = assertion.is_str('warn')

    #
    # property
    #

    @property
    def title(self) -> str:
        return self._title

    @property
    def outline(self) -> str:
        return self._outline

    @property
    def version(self) -> tuple:
        return self._version

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def is_plot(self) -> bool:
        return self._is_plot

    @property
    def is_text(self) -> bool:
        return self._is_text

    @property
    def is_scenario(self) -> bool:
        return self._is_scenario

    @property
    def is_audiodrama(self) -> bool:
        return self._is_audiodrama

    @property
    def is_rubi(self) -> bool:
        return self._is_rubi

    @property
    def is_comment(self) -> bool:
        return self._is_comment

    @property
    def is_console(self) -> bool:
        return self._is_console

    @property
    def format_mode(self) -> FormatMode:
        return self._format_mode

    @property
    def output_mode(self) -> OutputMode:
        return self._output_mode

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def builddir(self) -> str:
        return self._builddir

    @property
    def log_level(self) -> str:
        return self._log_level

    #
    # methods (story)
    #

    def set_title(self, title: str) -> None:
        self._title = assertion.is_str(title)

    def set_outline(self, outline: str) -> None:
        self._outline = assertion.is_str(outline)

    def set_version(self, *args: (str, int, tuple)) -> None:
        if isinstance(args[0], tuple):
            self._version = args[0]
        elif len(args) >= 3 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], int):
            self._version = (args[0], args[1], args[2])
        else:
            self._version = (assertion.is_str(args[0]),)

    def set_columns(self, col: int) -> None:
        self._columns = assertion.is_int(col)

    def set_rows(self, rows: int) -> None:
        self._rows = assertion.is_int(rows)

    def set_priority(self, pri: int) -> None:
        self._priority = assertion.is_between(
                assertion.is_int(pri), __PRIORITY_MAX__, __PRIORITY_MIN__)

    def set_start(self, start: int) -> None:
        self._start = assertion.is_int(start)

    def set_end(self, end: int) -> None:
        self._end = assertion.is_int(end)

    def set_base_date(self, month: int, day: int, year: int) -> None:
        self._base_date = datetime.date(year, month, day)

    def set_base_time(self, hour: int, minute: int) -> None:
        self._base_time = datetime.time(hour, minute)

    #
    # methods (compile)
    #

    def set_is_plot(self, is_plot: bool) -> None:
        self._is_plot = assertion.is_bool(is_plot)

    def set_is_text(self, is_text: bool) -> None:
        self._is_text = assertion.is_bool(is_text)

    def set_is_scenario(self, is_scenario: bool) -> None:
        self._is_scenario = assertion.is_bool(is_scenario)

    def set_is_audiodrama(self, is_audiodrama: bool) -> None:
        self._is_audiodrama = assertion.is_bool(is_audiodrama)

    def set_is_rubi(self, is_rubi: bool) -> None:
        self._is_rubi = assertion.is_bool(is_rubi)

    def set_is_comment(self, is_comment: bool) -> None:
        self._is_comment = assertion.is_bool(is_comment)

    def set_is_console(self, is_console: bool) -> None:
        self._is_console = assertion.is_bool(is_console)

    def set_format_mode(self, mode: FormatMode) -> None:
        self._format_mode = assertion.is_instance(mode, FormatMode)

    def set_output_mode(self, mode: OutputMode) -> None:
        self._output_mode = assertion.is_instance(mode, OutputMode)

    def set_filename(self, filename: str) -> None:
        self._filename = assertion.is_str(filename)

    def set_builddir(self, builddir: str) -> None:
        self._builddir = assertion.is_str(builddir)

    def set_log_level(self, loglevel: str) -> None:
        self._log_level = assertion.is_str(loglevel)
