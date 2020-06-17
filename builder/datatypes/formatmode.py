# -*- coding: utf-8 -*-
'''
Format Mode Enum
================
'''

from __future__ import annotations

__all__ = ('FormatMode',)


from enum import Enum, auto
from builder.utils import assertion


class FormatMode(Enum):
    ''' Format mode.
    '''
    DEFAULT = auto()
    PLAIN = auto()
    WEB = auto()
    SMARTPHONE = auto()

    @classmethod
    def get_all(cls) -> list:
        return [cls.DEFAULT, cls.PLAIN, cls.WEB, cls.SMARTPHONE]

    @classmethod
    def conv_to_mode(cls, mode: str) -> FormatMode:
        if assertion.is_str(mode) in ('w', 'web'):
            return FormatMode.WEB
        elif mode in ('s', 'smartphone', 'phone'):
            return FormatMode.SMARTPHONE
        elif mode in ('p', 'plain'):
            return FormatMode.PLAIN
        else:
            return FormatMode.DEFAULT
