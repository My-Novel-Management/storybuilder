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
        # for specific
        self._title = assertion.is_str(title)
        self._copy = assertion.is_str('__catch_copy__')
        self._oneline = assertion.is_str('__one_line__')
        self._outline = assertion.is_str('__story_outline__')
        self._theme = assertion.is_str('__theme__')
        self._genre = assertion.is_str('__genre__')
        self._target = assertion.is_str('__target_age__')
        self._size = assertion.is_str('__size__')
        self._desc_size = assertion.is_int(0)
        self._total_size = assertion.is_int(0)
        self._desc_papers = assertion.is_int_or_float(0)
        self._total_papers = assertion.is_int_or_float(0)
        # for story
        self._priority = assertion.is_int(__PRIORITY_DEFAULT__)
        self._start = assertion.is_int(0)
        self._end = assertion.is_int(-1)
        self._base_date = datetime.date(2020,1,1)
        self._base_time = datetime.time(12,00)
        self._version = assertion.is_tuple((0,0,1))
        self._columns = assertion.is_int(20)
        self._rows = assertion.is_int(20)
        self._contest_info = assertion.is_str('')
        self._caution = assertion.is_str('')
        self._note = assertion.is_str('')
        self._sites = assertion.is_listlike([])
        self._taginfos = assertion.is_listlike([])
        self._modified = datetime.date.today()
        self._released = datetime.date(2020,1,1)
        # for compile
        self._is_data = assertion.is_bool(False)
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
    # property (specific)
    #

    @property
    def title(self) -> str:
        return self._title

    @property
    def copy(self) -> str:
        return self._copy

    @property
    def oneline(self) -> str:
        return self._oneline

    @property
    def outline(self) -> str:
        return self._outline

    @property
    def theme(self) -> str:
        return self._theme

    @property
    def genre(self) -> str:
        return self._genre

    @property
    def target(self) -> str:
        return self._target

    @property
    def size(self) -> str:
        return self._size

    @property
    def desc_size(self) -> int:
        return self._desc_size

    @property
    def total_size(self) -> int:
        return self._total_size

    @property
    def desc_papers(self) -> (int, float):
        return self._desc_papers

    @property
    def total_papers(self) -> (int, float):
        return self._total_papers

    #
    # property (story)
    #

    @property
    def version(self) -> tuple:
        return self._version

    @property
    def contest_info(self) -> str:
        return self._contest_info

    @property
    def caution(self) -> str:
        return self._caution

    @property
    def note(self) -> str:
        return self._note

    @property
    def sites(self) -> (list, tuple):
        return self._sites

    @property
    def taginfos(self) -> (list, tuple):
        return self._taginfos

    @property
    def modified(self) -> datetime.date:
        return self._modified

    @property
    def released(self) -> datetime.date:
        return self._released

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
    def is_data(self) -> bool:
        return self._is_data

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
    # methods (specific)
    #

    def set_title(self, title: str) -> None:
        self._title = assertion.is_str(title)

    def set_theme(self, theme: str) -> None:
        self._theme = assertion.is_str(theme)

    def set_copy(self, copy: str) -> None:
        self._copy = assertion.is_str(copy)

    def set_oneline(self, oneline: str) -> None:
        self._oneline = assertion.is_str(oneline)

    def set_outline(self, outline: str) -> None:
        self._outline = assertion.is_str(outline)

    def set_genre(self, genre: str) -> None:
        self._genre = assertion.is_str(genre)

    def set_target(self, target: str) -> None:
        self._target = assertion.is_str(target)

    def set_size(self, size: str) -> None:
        self._size = assertion.is_str(size)

    def set_desc_size(self, size: int) -> None:
        self._desc_size = assertion.is_int(size)

    def set_total_size(self, size: int) -> None:
        self._total_size = assertion.is_int(size)

    def set_desc_papers(self, papers: (int, float)) -> None:
        self._desc_papers = assertion.is_int_or_float(papers)

    def set_total_papers(self, papers: (int, float)) -> None:
        self._total_papers = assertion.is_int_or_float(papers)

    #
    # methods (story)
    #

    def set_version(self, *args: (str, int, tuple)) -> None:
        if isinstance(args[0], tuple):
            self._version = args[0]
        elif len(args) >= 3 and isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], int):
            self._version = (args[0], args[1], args[2])
        else:
            self._version = (assertion.is_str(args[0]),)

    def set_contest_info(self, info: str) -> None:
        self._contest_info = assertion.is_str(info)

    def set_caution(self, info: str) -> None:
        self._caution = assertion.is_str(info)

    def set_note(self, note: str) -> None:
        self._note = assertion.is_str(note)

    def set_sites(self, *args: str) -> None:
        self._sites = [assertion.is_str(val) for val in args]

    def set_taginfos(self, *args: str) -> None:
        if isinstance(args[0], (list, tuple)):
            self._taginfos = args[0]
        else:
            self._taginfos = [v for v in args if isinstance(v, str)]

    def set_modified(self, *args: (datetime.date, int)) -> None:
        if isinstance(args[0], datetime.date):
            self._modified = args[0]
        else:
            y, m, d = assertion.is_int(args[2]), assertion.is_int(args[0]), assertion.is_int(args[1])
            self._modified = datetime.date(y, m, d)

    def set_released(self, *args: (datetime.date, int)) -> None:
        if isinstance(args[0], datetime.date):
            self._released = args[0]
        else:
            y, m, d = assertion.is_int(args[2]), assertion.is_int(args[0]), assertion.is_int(args[1])
            self._released = datetime.date(y, m, d)

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

    def set_is_data(self, is_data: bool) -> None:
        self._is_data = assertion.is_bool(is_data)

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
