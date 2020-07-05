# -*- coding: utf-8 -*-
'''
Counter Object
==============
'''

from __future__ import annotations

__all__ = ('Counter',)


from analyzer.datatypes.mecabdata import MecabData
from analyzer.datatypes.wordclass import WordClass
from analyzer.datatypes.tokenlist import TokenList
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.util_str import kanji_list_from
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class WordCounter(object):
    ''' Word Counter Object class.
    '''

    #
    # methods (word classes)
    #

    def word_classes_of(self, src: TokenList, wordclass: WordClass) -> int:
        tmp = []
        assertion.is_instance(wordclass, WordClass)
        for token in assertion.is_instance(src, TokenList).data:
            if assertion.is_instance(token, MecabData).wordclass == wordclass.conv_str():
                tmp.append(token)
        return len(tmp)

    #
    # methods (kanji)
    #

    def kanjis_of(self, src: (TextList, list, tuple, str)) -> int:
        tmp = []
        if isinstance(src, TextList):
            tmp = [kanji_list_from(line) for line in src.data]
        elif isinstance(src, (list, tuple)):
            tmp = [kanji_list_from(line) for line in src]
        elif isinstance(src, str):
            tmp = kanji_list_from(src)
        else:
            return 0
        return len(tmp)
