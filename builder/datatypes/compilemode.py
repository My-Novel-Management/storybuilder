# -*- coding: utf-8 -*-
'''
Compile Mode Enum
=================
'''

from __future__ import annotations

__all__ = ('CompileMode',)


from enum import Enum, auto


class CompileMode(Enum):
    ''' Compile Mode enumerate
    '''
    NORMAL = auto()
    NOVEL_TEXT = auto()
    STORY_DATA = auto()
    PLOT = auto()
    SCENARIO = auto()
    AUDIODRAMA = auto()

    @classmethod
    def get_all(cls) -> list:
        return [cls.NORMAL, cls.NOVEL_TEXT,
                cls.STORY_DATA,
                cls.PLOT,
                cls.SCENARIO, cls.AUDIODRAMA]
