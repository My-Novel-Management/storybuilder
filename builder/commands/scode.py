# -*- coding: utf-8 -*-
'''
Story Code Object
=================
'''

from __future__ import annotations

__all__ = ('SCode',)


from builder.commands.command import SCmd
from builder.objects.sobject import SObject
from builder.utils import assertion


class SCode(SObject):
    ''' Story Code Object class.
    '''
    def __init__(self,
            src: SObject,
            cmd: SCmd,
            script: tuple,
            option: (int, str)='',
            ):
        super().__init__('__scode__')
        self._src = assertion.is_instance(src, SObject) if src else None
        self._cmd = assertion.is_instance(cmd, SCmd)
        self._script = assertion.is_tuple(script)
        self._option = assertion.is_int_or_str(option)

    #
    # property
    #
    @property
    def src(self) -> (SObject, None):
        return self._src

    @property
    def cmd(self) -> str:
        return self._cmd

    @property
    def script(self) -> tuple:
        return self._script

    @property
    def option(self) -> str:
        return self._option

    #
    # methods
    #

    def inherited(self,
            src: SObject=None,
            script: tuple=None,
            option: str=None) -> SCode:
        return SCode(
                src if src else self.src,
                self.cmd,
                script if script else self.script,
                option if option else self.option,
                )

