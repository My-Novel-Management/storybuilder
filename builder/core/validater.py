# -*- coding: utf-8 -*-
'''
Validater Object
================
'''

from __future__ import annotations

__all__ = ('Validater',)


from typing import Tuple
from builder.commands.scode import SCode, SCmd
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.formattag import FormatTag
from builder.datatypes.resultdata import ResultData
from builder.tools.checker import Checker
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class ValidaterError(BuilderError):
    ''' General Validate Error.
    '''
    pass


class InvalidSymbolError(ValidaterError):
    ''' Has invalid symbol.
    '''
    pass


class Validater(Executer):
    ''' Description Validater Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('VALIDATER: initialize')

    #
    # methods
    #

    def execute(self, src: CodeList) -> ResultData:
        LOG.info('VALIDATER: start exec')

        is_succeeded = True
        error = None
        ret, is_succeeded = self._has_invalid_symbol(src)

        if not is_succeeded:
            msg = f'Invalid symbol: {ret}'
            LOG.error(msg)
            error = InvalidSymbolError(msg)
        return ResultData(
                ret,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _has_invalid_symbol(self, src: CodeList) -> Tuple[list, bool]:
        tmp = []
        invalids = []
        checker = Checker()

        for child in assertion.is_instance(src, CodeList).data:
            assertion.is_instance(child, SCode)
            if child.cmd in SCmd.get_all_actions():
                for line in child.script:
                    if checker.has_tag_symbol(line):
                        invalids.append(line)
                tmp.append(child)
            else:
                # NOTE: それ以外をどうするか。ここはスルーか
                tmp.append(child)
        if invalids:
            return (invalids, False)
        else:
            return (CodeList(*tmp), True)
