# -*- coding: utf-8 -*-
'''
Stage Object
============
'''

from __future__ import annotations

__all__ = ('Stage',)


from builder.objects.sobject import SObject
from builder.utils import assertion


class Stage(SObject):
    ''' Stage Object class.
    '''

    def __init__(self,
            name: str,
            parent: str='',
            geometry: tuple=None,
            info: str=''):
        super().__init__(name)
        self._parent = assertion.is_str(parent)
        self._geometry = assertion.is_tuple(geometry) if geometry else (0,0)
        self._info = assertion.is_str(info)

    #
    # property
    #

    @property
    def parent(self) -> str:
        return self._parent

    @property
    def geometry(self) -> tuple:
        return self._geometry

    @property
    def info(self) -> str:
        return self._info

