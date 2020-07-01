# -*- coding: utf-8 -*-
'''
MaterialType Enum
=================
'''

from __future__ import annotations

__all__ = ('MaterialType',)


from enum import Enum, auto


class MaterialType(Enum):
    ''' Material Type enumerate
    '''
    DOCUMENT = auto()
    WRITER_NOTE = auto()
    CHARACTER_NOTE = auto()

    @classmethod
    def get_all(cls) -> list:
        return [
                cls.WRITER_NOTE, cls.CHARACTER_NOTE,
                cls.DOCUMENT,
                ]
