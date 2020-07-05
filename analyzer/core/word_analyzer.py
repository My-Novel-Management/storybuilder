# -*- coding: utf-8 -*-
'''
Word Analyzer Object
================
'''

from __future__ import annotations

__all__ = ('WordAnalyzer',)


from analyzer.datatypes.analyzerexception import AnalyzerError
from analyzer.datatypes.mecabdata import MecabData
from analyzer.datatypes.tokenlist import TokenList
from analyzer.datatypes.wordclass import WordClass
from analyzer.tools.counter import WordCounter
from builder.core.executer import Executer
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class WordAnalyzeError(AnalyzerError):
    ''' General error in WordAnalyzer.
    '''
    pass


class WordAnalyzer(Executer):
    ''' Word Analyze class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('WORD_ANALYZER: initialize')

    #
    # methods
    #

    def execute(self, src: TokenList) -> ResultData:
        LOG.info('WORD_ANALYZER: start exec')
        is_succeeded = True
        error = None
        tmp = assertion.is_listlike(self._exec_internal(src))
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: TokenList) -> list:
        LOG.debug(f'-- src: {src}')
        tmp = []
        tmp.extend(self._wordclass_counts(src))
        return tmp

    def _wordclass_counts(self, src: TokenList) -> list:
        assertion.is_instance(src, TokenList)
        tmp = []
        counter = WordCounter()
        # 品詞数
        total = len(src.data)
        each_nums = [(wcls, counter.word_classes_of(src, wcls)) for wcls in WordClass.get_all()]
        tmp.append('# 品詞分析\n')
        tmp.append(f'- Total: {total}')
        for val in each_nums:
            tmp.append(f'- {val[0].conv_str()}: {val[1]}')
        return tmp

