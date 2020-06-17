# -*- coding: utf-8 -*-
'''
Word Object
===========
'''

from __future__ import annotations

__all__ = ('Word',)


from builder.objects.sobject import SObject
from builder.utils import assertion


class Word(SObject):
    ''' Word Object class.
    '''

    def __init__(self,
            name: str,
            category: str='',
            info: str=''):
        super().__init__(name)
        self._category = assertion.is_str(category)
        self._info = assertion.is_str(info)

    #
    # property
    #

    @property
    def category(self) -> str:
        return self._category

    @property
    def info(self) -> str:
        return self._info

