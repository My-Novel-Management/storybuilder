# -*- coding: utf-8 -*-
'''
Format Tag Enum
===============
'''

from __future__ import annotations

__all__ = ('FormatTag',)


from enum import Enum, auto
from builder.utils import assertion


class FormatTag(Enum):
    ''' Format tag enumerate.
    '''
    DESCRIPTION_HEAD = auto()
    DIALOGUE_HEAD = auto()
    SYMBOL_HEAD = auto()
    TAG_HEAD = auto()

    @classmethod
    def get_all(cls) -> list:
        return [cls.DESCRIPTION_HEAD, cls.DIALOGUE_HEAD,
                cls.SYMBOL_HEAD, cls.TAG_HEAD]

