# -*- coding: utf-8 -*-
'''
Frequency Analyzer Object
=========================
'''

from __future__ import annotations

__all__ = ('FrequencyAnalyzer',)


from collections import Counter
from analyzer.datatypes.analyzerexception import AnalyzerError
from analyzer.datatypes.mecabdata import MecabData
from analyzer.datatypes.tokenlist import TokenList
from analyzer.datatypes.wordclass import WordClass
from analyzer.tools.counter import WordCounter
from builder.core.executer import Executer
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion
from builder.utils.util_str import kanji_list_from, katakana_list_from, hiragana_list_from
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class FreqencyAnalyzeError(AnalyzerError):
    ''' General error in FrequencyAnalyzer.
    '''
    pass


class FrequencyAnalyzer(Executer):
    ''' Frequency Analyze class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('FREQ_ANALYZER: initialize')

    #
    # methods
    #

    def execute(self, src: TokenList) -> ResultData:
        LOG.info('FREQ_ANALYZER: start exec')
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
        assertion.is_instance(src, TokenList)
        tmp = []
        tmp.append('# 頻度分析\n')
        for wcls in WordClass.get_all():
            lst = [token for token in src.data if token.wordclass == wcls.conv_str()]
            if wcls.conv_str() == '名詞':
                lst = [token for token in lst if not (self._is_person_name(token) or self._is_pronoun(token) or self._is_not_independence(token) or self._is_suffix(token))]
            cnt = Counter([token.basic_type for token in lst])
            idx = 0
            w_tmp = []
            tmp.append(f'* {wcls.conv_str()}')
            for word, num in cnt.most_common():
                if idx >= 10:
                    break
                w_tmp.append(f'{word}({num})')
                idx += 1
            tmp.append(f'    - {"／".join(w_tmp)}')
        return tmp

    def _is_person_name(self, token: MecabData) -> bool:
        return assertion.is_instance(token, MecabData).class_detail1 == '固有名詞' and token.class_detail2 == '人名'

    def _is_pronoun(self, token: MecabData) -> bool:
        return assertion.is_instance(token, MecabData).class_detail1 == '代名詞'

    def _is_not_independence(self, token: MecabData) -> bool:
        return assertion.is_instance(token, MecabData).class_detail1 == '非自立'

    def _is_suffix(self, token: MecabData) -> bool:
        return assertion.is_instance(token, MecabData).class_detail1 == '接尾'
