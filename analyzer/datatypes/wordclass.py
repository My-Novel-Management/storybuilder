# -*- coding: utf-8 -*-
'''
Word Class Enum
===============
'''

from __future__ import annotations

__all__ = ('WordClass',)


from enum import Enum, auto
from builder.utils import assertion


class WordClass(Enum):
    ''' Word class enumerate.
    '''
    NOUN = auto() # 名詞
    VERB = auto() # 動詞
    ADJECTIVE = auto() # 形容詞
    ADVERB = auto() # 副詞
    CONJUCTION = auto() # 接続詞
    INTERJECTION = auto() # 感動詞
    ADNOMINAL = auto() # 連体詞
    AUXVERB = auto() # 助動詞
    PARTICLE = auto() # 助詞
    MARK = auto() # 記号
    PREFIX = auto() # 接頭詞
    FILLER = auto() # フィラー
    OTHER = auto() # その他

    @classmethod
    def get_all(cls) -> list:
        return [cls.NOUN, cls.VERB, cls.ADJECTIVE, cls.ADVERB,
                cls.CONJUCTION, cls.INTERJECTION, cls.ADNOMINAL,
                cls.AUXVERB, cls.PARTICLE,
                cls.MARK, cls.PREFIX,
                cls.FILLER, cls.OTHER]

    def conv_str(self) -> str:
        return {
                WordClass.NOUN: "名詞",
                WordClass.VERB: "動詞",
                WordClass.ADJECTIVE: "形容詞",
                WordClass.ADVERB: "副詞",
                WordClass.CONJUCTION: "接続詞",
                WordClass.INTERJECTION: "感動詞",
                WordClass.ADNOMINAL: "連体詞",
                WordClass.AUXVERB: "助動詞",
                WordClass.PARTICLE: "助詞",
                WordClass.MARK: "記号",
                WordClass.PREFIX: "接続詞",
                WordClass.FILLER: "フィラー",
                WordClass.OTHER: "その他",
                }[self]
