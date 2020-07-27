# -*- coding: utf-8 -*-
'''
Outputter Object
================
'''

from __future__ import annotations

__all__ = ('Outputter',)

import datetime
import os
from enum import Enum, auto
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.outputmode import OutputMode
from builder.datatypes.resultdata import ResultData
from builder.datatypes.rawdata import RawData
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class OutputModeError(BuilderError):
    ''' Exception of output-mode mismatch.
    '''
    pass


class Outputter(Executer):
    ''' Outputter Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('OUTPUT: initialize')

    #
    # methods
    #

    def execute(self, src: TextList, mode: OutputMode,
            filename: str, suffix: str, extention: str,
            builddir: str) -> ResultData:
        LOG.info('OUTPUT: start exec')
        is_succeeded = True
        tmp = []
        error = None
        if assertion.is_instance(mode, OutputMode) is OutputMode.CONSOLE:
            is_succeeded = self._out_to_console(src)
        elif mode is OutputMode.FILE:
            is_succeeded = self._out_to_file(src, filename, suffix,
                    extention, builddir)
        else:
            msg = f'Unknown OutputMode!: {mode}'
            LOG.critical(msg)
            error = OutputModeError(msg)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _out_to_console(self, src: TextList) -> bool:
        LOG.info('OUTPUT: out to console')

        is_succeeded = True
        for line in assertion.is_instance(src, TextList).data:
            print(line, end='')
        print(datetime.datetime.now())
        return is_succeeded

    def _out_to_file(self, src: TextList,
            filename: str, suffix: str, extention: str,
            builddir: str) -> bool:
        LOG.info('OUTPUT: out to file')

        is_succeeded = True
        if not os.path.isdir(assertion.is_str(builddir)):
            os.makedirs(builddir)
        fullpath = os.path.join(builddir, "{}{}.{}".format(
            assertion.is_str(filename), assertion.is_str(suffix),
            assertion.is_str(extention)
            ))
        with open(fullpath, 'w') as f:
            for line in assertion.is_instance(src, TextList).data:
                f.write(f"{line}")
            f.write(f'{datetime.datetime.now()}')
        return is_succeeded

