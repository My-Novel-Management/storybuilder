# -*- coding: utf-8 -*-
'''
Percent Analyzer Object
=======================
'''

from __future__ import annotations

__all__ = ('PercentAnalyzer',)


from analyzer.datatypes.analyzerexception import AnalyzerError
from analyzer.datatypes.mecabdata import MecabData
from analyzer.datatypes.wordclass import WordClass
from analyzer.tools.counter import WordCounter
from builder.core.executer import Executer
from builder.datatypes.resultdata import ResultData
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.util_math import safe_divided
from builder.utils.util_str import kanji_list_from, katakana_list_from, hiragana_list_from
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class PercentAnalyzeError(AnalyzerError):
    ''' General error in PercentAnalyzer.
    '''
    pass


class PercentAnalyzer(Executer):
    ''' Percent Analyze class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('PERCENT_ANALYZER: initialize')

    #
    # methods
    #

    def execute(self, src: TextList) -> ResultData:
        LOG.info('PERCENT_ANALYZER: start exec')
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

    def _exec_internal(self, src: TextList) -> list:
        LOG.debug(f'-- src: {src}')
        tmp = []
        tmp.append('# 割合データ\n')
        tmp.extend(self._kanji_percents(src))
        tmp.append('')
        tmp.extend(self._dialogue_percents(src))
        tmp.append('')
        return tmp

    def _kanji_percents(self, src: TextList) -> list:
        assertion.is_instance(src, TextList)
        tmp = []
        totals = sum([len(self._rid_topspace(line)) for line in src.data])
        kanjis = 0
        katakanas = 0
        hiraganas = 0
        for line in src.data:
            kanjis += sum(len(v) for v in kanji_list_from(line))
            katakanas += sum(len(v) for v in katakana_list_from(line))
            hiraganas += sum(len(v) for v in hiragana_list_from(line))
        kanji_per = safe_divided(kanjis, totals) * 100
        katakana_per = safe_divided(katakanas, totals) * 100
        hiragana_per = safe_divided(hiraganas, totals) * 100
        tmp.append('## カナ・漢字\n')
        tmp.append(f"- Total: {totals}c")
        tmp.append(f'- Kanji: {kanji_per:.2f}% [{kanjis}c]')
        tmp.append(f'- Katakana: {katakana_per:.2f}% [{katakanas}c]')
        tmp.append(f'- Hiragana: {hiragana_per:.2f}% [{hiraganas}c]')
        return tmp

    def _dialogue_percents(self, src: TextList) -> list:
        assertion.is_instance(src, TextList)
        tmp = []
        def _is_desc(val):
            return val.startswith('　')
        def _is_dialogue(val):
            return val.startswith(('「', '『'))
        totals = len([line for line in src.data])
        total_chars = sum([len(self._rid_topspace(line)) for line in src.data])
        descriptions = len([line for line in src.data if _is_desc(line)])
        desc_chars = sum([len(self._rid_topspace(line)) for line in src.data if _is_desc(line)])
        dialogues = len([line for line in src.data if _is_dialogue(line)])
        dial_chars = sum([len(line) for line in src.data if _is_dialogue(line)])
        desc_per = safe_divided(desc_chars, total_chars) * 100
        dial_per = safe_divided(dial_chars, total_chars) * 100
        tmp.append('## 台詞\n')
        tmp.append(f'- Total      : {total_chars}c / {totals}line')
        tmp.append(f'- Description: {desc_per:.2f}% [{desc_chars}c / {descriptions}line]')
        tmp.append(f'- Dialogue   : {dial_per:.2f}% [{dial_chars}c / {dialogues}line]')
        return tmp

    def _rid_topspace(self, src: str):
        if assertion.is_str(src).startswith('　'):
            if src.startswith('　　　　'):
                return src[4:]
            else:
                return src[1:]
        else:
            return src
