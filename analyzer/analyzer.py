# -*- coding: utf-8 -*-
'''
Analyzer Object
===============
'''

from __future__ import annotations

__all__ = ('Analyzer',)

import os
from analyzer.core.tokenizer import Tokenizer
from analyzer.core.word_analyzer import WordAnalyzer
from analyzer.datatypes.analyzerexception import AnalyzerError
from analyzer.datatypes.tokenlist import TokenList
from builder.core.executer import Executer
from builder.core.outputter import Outputter
from builder.datatypes.outputmode import OutputMode
from builder.datatypes.rawdata import RawData
from builder.datatypes.resultdata import ResultData
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.util_file import get_content_from_text_file
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Analyzer(Executer):
    ''' Analyzer object.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('ANALYZER: initialize')

    def execute(self, src: (str, list, TextList),
            is_debug: bool=False) -> ResultData: # pragma: no cover
        LOG.info('ANALYZER: start exec')
        is_succeeded = True
        error = None
        basesrc = None
        result = ResultData([], is_succeeded, error)
        tokenizer = Tokenizer()

        if isinstance(src, str):
            basesrc = TextList(*get_content_from_text_file(src))
        elif isinstance(src, TextList):
            basesrc = src
        elif isinstance(src, (list, tuple)):
            basesrc = TextList(*src)
        else:
            msg = f'Invalid analyze source!: {src}'
            LOG.critical(msg)
            return ResultData(result, False, AnalyzerError(msg))

        tmp = self._rid_tag(basesrc)

        LOG.info('TOKENIZER: call')
        result = assertion.is_instance(tokenizer.execute(tmp), ResultData)
        if not result.is_succeeded:
            return result
        tokens = assertion.is_instance(result.data, TokenList)

        LOG.info('WORD_ANALYZER: call')
        result = assertion.is_instance(WordAnalyzer().execute(tokens), ResultData)
        if not result.is_succeeded:
            return result
        tmp = result.data

        LOG.info('Analyzer result output')
        fname = 'result'
        suffix = ''
        extention = 'md'
        builddir = 'build/results'
        mode = OutputMode.CONSOLE if is_debug else OutputMode.FILE
        data = TextList(*[f'{line}\n' for line in tmp])
        Outputter().execute(data, mode, fname, suffix, extention, builddir)
        return result

    #
    # private
    #

    def _rid_tag(self, src: TextList) -> TextList:
        LOG.info('ANALYZER: rid tags start')
        tmp = []
        for line in assertion.is_instance(src, TextList).data:
            assertion.is_str(line)
            if line.startswith('#'):
                continue
            else:
                tmp.append(line)
        return TextList(*tmp)
