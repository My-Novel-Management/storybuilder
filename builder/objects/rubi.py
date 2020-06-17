# -*- coding: utf-8 -*-
'''
Rubi Object
===========
'''

from __future__ import annotations

__all__ = ('Rubi',)


from builder.objects.sobject import SObject
from builder.utils import assertion


class Rubi(SObject):
    ''' Rubi Object class.
    '''

    def __init__(self, name: str, rubi: str, exclusions: tuple=None,
            is_always: bool=False):
        super().__init__(name)
        self._rubi = assertion.is_str(rubi)
        self._exclusions = assertion.is_tuple(exclusions) if exclusions else ()
        self._is_always = assertion.is_bool(is_always)

    #
    # property
    #

    @property
    def rubi(self) -> str:
        return self._rubi

    @property
    def exclusions(self) -> tuple:
        return self._exclusions

    @property
    def is_always(self) -> bool:
        return self._is_always

    #
    # methods
    #

