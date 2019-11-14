# -*- coding: utf-8 -*-
"""Define flag class.
"""
from . import assertion
from .basedata import BaseData


class Flag(BaseData):
    """Data type of flags.
    """
    __NAME__ = "__flag__"
    def __init__(self, info: str, isDeflag: bool=False):
        super().__init__(Flag.__NAME__)
        self._info = assertion.is_str(info)
        self._isDeflag = assertion.is_bool(isDeflag)

    @property
    def info(self): return self._info

    @property
    def isDeflag(self): return self._isDeflag


class NoFlag(Flag):
    """Nothing data.
    """
    __NAME__ = "__noflag__"
    def __init__(self):
        super().__init__(NoFlag.__NAME__)


class NoDeflag(Flag):
    """Nothing data.
    """
    __NAME__ = "__nodeflag__"
    def __init__(self):
        super().__init__(NoDeflag.__NAME__, True)
