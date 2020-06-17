# -*- coding: utf-8 -*-
'''
Writer Object
=============
'''

from __future__ import annotations

__all__ = ('Writer',)


from typing import Any
from builder.commands.command import SCmd
from builder.commands.scode import SCode
from builder.objects.sobject import SObject
from builder.utils import assertion


class Writer(object):
    ''' Writer Object class.
    '''

    def __init__(self, src: SObject):
        self._src = assertion.is_instance(src, SObject)

    #
    # methods
    #

    def be(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.BE, args)

    def come(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.COME, args)

    def do(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.DO, args)

    def explain(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.EXPLAIN, args)

    def go(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.GO, args)

    def hear(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.HEAR, args)

    def look(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.LOOK, args)

    def talk(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.TALK, args)

    def think(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.THINK, args)

    def voice(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.VOICE, args)

    def wear(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.WEAR, args)

