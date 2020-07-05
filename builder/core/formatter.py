# -*- coding: utf-8 -*-
'''
Formatter Object
================
'''

from __future__ import annotations

__all__ = ('Reducer',)


from enum import Enum, auto
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.formatmode import FormatMode
from builder.datatypes.formattag import FormatTag
from builder.datatypes.rawdata import RawData
from builder.datatypes.resultdata import ResultData
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class FormatModeError(BuilderError):
    ''' Exception class for Format
    '''
    pass


class Formatter(Executer):
    ''' Formatter Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('FORMATTER: initialize')

    #
    # methods
    #

    def execute(self, src: RawData, mode: FormatMode) -> ResultData:
        LOG.info(f'FORMATTER: start exec on [{mode}] mode')
        LOG.debug(f'-- src: {src}')

        is_succeeded = True
        tmp = []
        error = None

        if mode is FormatMode.DEFAULT:
            tmp = assertion.is_instance(self._to_default(src), TextList)
        elif mode is FormatMode.PLAIN:
            tmp = src
        elif mode is FormatMode.WEB:
            tmp = assertion.is_instance(self._to_web(src), TextList)
        elif mode is FormatMode.SMARTPHONE:
            tmp = src
        else:
            msg = f'Invalid format-mode! {mode}'
            LOG.critical(msg)
            is_succeeded = False
            error = FormatModeError(msg)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _to_default(self, src: RawData) -> TextList:
        LOG.info('FORMAT: to_default')
        tmp = []
        for line in assertion.is_instance(src, RawData).data:
            if isinstance(line, FormatTag):
                continue
            else:
                tmp.append(line)
        return TextList(*tmp)

    def _to_web(self, src: RawData) -> TextList:
        LOG.info('FORMAT: to_web')

        tmp = []
        in_dialogue = False

        for line in assertion.is_instance(src, RawData).data:
            if isinstance(line, FormatTag):
                if line is FormatTag.DESCRIPTION_HEAD:
                    if in_dialogue:
                        tmp.append('\n')
                        in_dialogue = False
                elif line is FormatTag.DIALOGUE_HEAD:
                    if not in_dialogue:
                        tmp.append('\n')
                        in_dialogue = True
                elif line is FormatTag.SYMBOL_HEAD:
                    pass
                elif line is FormatTag.TAG_HEAD:
                    pass
                else:
                    pass
            else:
                assertion.is_str(line)
                tmp.append(line)
        return TextList(*tmp)
