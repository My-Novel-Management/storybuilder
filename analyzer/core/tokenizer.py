# -*- coding: utf-8 -*-
'''
Tokenizer Object
================
'''

from __future__ import annotations

__all__ = ('Tokenizer',)


import os
import re
import MeCab
from analyzer.datatypes.analyzerexception import AnalyzerError
from analyzer.datatypes.mecabdata import MecabData
from analyzer.datatypes.tokenlist import TokenList
from analyzer.datatypes.wordclass import WordClass
from builder.core.executer import Executer
from builder.datatypes.resultdata import ResultData
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class TokenizerError(AnalyzerError):
    ''' General error in Tokenizer.
    '''
    pass


class Tokenizer(Executer):
    ''' Tokenizer class.
    '''
    __MECAB_DIRS__ = (
            "/usr/local/lib/mecab/dic/mecab-ipadic-neologd",
            "/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd",
            )

    def __init__(self):
        super().__init__()
        LOG.info('TOKENIZER: initialize')
        self._tagger = None

    #
    # methods
    #

    def execute(self, src: (TextList, list, tuple), person_names: list,
            mecab_dir: str=None) -> ResultData:
        LOG.info('TOKENIZER: start exec')
        is_succeeded = True
        error = None
        if not self._tagger:
            mdir = self._get_mecab_dir(mecab_dir)
            mdir = f'-d {mdir}' if mdir else ''
            self._tagger = MeCab.Tagger(mdir)
            self._tagger.parse('') # 初期化処理
        tmp = assertion.is_instance(self._exec_internal(src, person_names), TokenList)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: (TextList, list, tuple), person_names: list) -> TokenList:
        LOG.debug(f'-- src: {src}')
        tmp = []
        def _excepted(target: str):
            return target in ('EOS', '', 't', 'ー')
        def _is_exists_name(target: str):
            for name in person_names:
                if name == target:
                    return True
            return False
        _src = src.data if isinstance(src, TextList) else src
        parsed = self._tagger.parse('\n'.join(assertion.is_listlike(_src))).split('\n')
        tokens = self._packed_from_parsed(parsed)
        for token in tokens:
            if _excepted(token[0]):
                continue
            elif len(token) == 1:
                continue
            if token[1] == WordClass.NOUN.conv_str():
                if _is_exists_name(token[0]):
                    token[3] = '人名'
            tmp.append(MecabData.conv(*token))
        return TokenList(*tmp)

    def _get_mecab_dir(self, dirname: str) -> str:
        if dirname and os.path.exists(dirname):
            return dirname
        elif os.path.exists(self.__MECAB_DIRS__[0]):
            return self.__MECAB_DIRS__[0]
        elif os.path.exists(self.__MECAB_DIRS__[1]):
            return self.__MECAB_DIRS__[1]
        else:
            LOG.error('Not set MeCab dictionary path')
            return ''

    def _packed_from_parsed(self, src: list) -> tuple:
        return (re.split('[\t,]', v) for v in assertion.is_listlike(src))
