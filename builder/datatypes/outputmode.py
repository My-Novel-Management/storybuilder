# -*- coding: utf-8 -*-
'''
Output Mode Enum
================
'''

from __future__ import annotations

__all__ = ('OutputMode',)


from enum import Enum, auto


class OutputMode(Enum):
    ''' Output mode.
    '''
    CONSOLE = auto()
    FILE = auto()

    @classmethod
    def get_all(cls) -> list:
        return [cls.CONSOLE, cls.FILE]
