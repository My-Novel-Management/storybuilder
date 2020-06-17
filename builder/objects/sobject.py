# -*- coding: utf-8 -*-
'''
Story Object
============
'''

from __future__ import annotations

__all__ = ('SObject',)


from builder import __PRIORITY_DEFAULT__, __PRIORITY_MAX__, __PRIORITY_MIN__
from builder.utils import assertion


class SObject(object):
    ''' Story Object class.
    '''

    def __init__(self, name: str):
        self._name = assertion.is_str(name)
        self._priority = assertion.is_int(__PRIORITY_DEFAULT__)

    #
    # property
    #

    @property
    def name(self) -> str:
        return self._name

    @property
    def priority(self) -> int:
        return self._priority

    #
    # methods
    #

    def set_priority(self, pri: int) -> SObject:
        ''' Set the object priority.
        '''
        self._priority = assertion.is_between(
                assertion.is_int(pri),
                __PRIORITY_MAX__, __PRIORITY_MIN__)
        return self

    def omit(self) -> SObject:
        ''' Set the lowest priority for omit object.
        '''
        self._priority = assertion.is_int(__PRIORITY_MIN__)
        return self

