# -*- coding: utf-8 -*-
'''
MeCab token Data
================
'''

from __future__ import annotations

__all__ = ('MecabData',)


from builder.utils.logger import MyLogger
from builder.utils import assertion


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class MecabData(object):
    ''' Mecab token Data class.

    NOTE:
        - 表層形（単語）
        - 品詞
        - 品詞細分類１
        - 品詞細分類２
        - 品詞細分類３
        - 活用型
        - 活用形
        - 基本形
        - 読み
        - 発音
    '''
    def __init__(self,
            word: str,
            wordclass: str,
            class_detail1: str,
            class_detail2: str,
            class_detail3: str,
            grammer_type: str,
            conjugation: str,
            basic_type: str,
            reading: str=None,
            pronounce: str=None,
            options: str=None,
            ):
        self._word = assertion.is_str(word)
        self._wordclass = assertion.is_str(wordclass)
        self._class_detail1 = assertion.is_str(class_detail1)
        self._class_detail2 = assertion.is_str(class_detail2)
        self._class_detail3 = assertion.is_str(class_detail3)
        self._grammer_type = assertion.is_str(grammer_type)
        self._conjugation = assertion.is_str(conjugation)
        self._basic_type = assertion.is_str(basic_type)
        self._reading = assertion.is_str(reading) if reading else self._word
        self._pronounce = assertion.is_str(pronounce) if pronounce else self._word
        self._options = options
        if options:
            LOG.critical(f"Unknown mecab arguments: {options}")

    @classmethod
    def conv(cls, *args) -> MecabData:
        if not args or args[0] == '':
            return MecabData('', '', '', '', '', '', '', '', '', '')
        elif args[0] == 'EOS':
            return MecabData('EOS', '', '', '', '', '', '', '', '', '')
        else:
            return MecabData(*args)

    #
    # property
    #

    @property
    def word(self) -> str:
        return self._word

    @property
    def wordclass(self) -> str:
        return self._wordclass

    @property
    def class_detail1(self) -> str:
        return self._class_detail1

    @property
    def class_detail2(self) -> str:
        return self._class_detail2

    @property
    def class_detail3(self) -> str:
        return self._class_detail3

    @property
    def grammer_type(self) -> str:
        return self._grammer_type

    @property
    def conjugation(self) -> str:
        return self._conjugation

    @property
    def basic_type(self) -> str:
        return self._basic_type

    @property
    def reading(self) -> str:
        return self._reading

    @property
    def pronounce(self) -> str:
        return self._pronounce

    @property
    def mecab_data(self) -> str:
        tmp = ','.join([self.wordclass, self.class_detail1, self.class_detail2, self.class_detail3,
            self.grammer_type, self.conjugation, self.basic_type, self.reading, self.pronounce])
        return f'{self.word}\t{tmp}'

