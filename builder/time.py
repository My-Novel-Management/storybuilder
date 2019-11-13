# -*- coding: utf-8 -*-
"""Define time class.
"""
from . import assertion
from .basedata import BaseData


class Time(BaseData):
    """Data type of a time.
    """
    DEF_NUMSYS = 60

    def __init__(self, name: str, hour: int=0, min: int=0, sec: int=0):
        super().__init__(name)
        self._hour = assertion.is_int(hour)
        self._min = assertion.is_int(min)
        self._sec = assertion.is_int(sec)
        self._numsys = Time.DEF_NUMSYS

    @property
    def hour(self): return self._hour

    @property
    def min(self): return self._min

    @property
    def sec(self): return self._sec

    @property
    def numsys(self): return self._numsys

