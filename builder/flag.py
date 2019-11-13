# -*- coding: utf-8 -*-
"""Define flag class.
"""
from . import assertion
from .basedata import BaseData


class Flag(BaseData):
    """Data type of flags.
    """
    def __init__(self, info: str, isDeflag: bool=False):
        super().__init__("__flag__")
        self._info = assertion.is_str(info)
        self._isDeflag = isDeflag

    @property
    def info(self): return self._info

    @property
    def isDeflag(self): return self._isDeflag


class NoFlag(Flag):
    """Nothing data.
    """
    def __init__(self):
        super().__init__("")


class NoDeflag(Flag):
    """Nothing data.
    """
    def __init__(self):
        super().__init__("", True)
