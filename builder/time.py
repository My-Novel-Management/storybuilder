# -*- coding: utf-8 -*-
"""Define time class.
"""
from . import assertion
from .basedata import BaseData


class Time(BaseData):
    """Data type of a time.
    """
    __DEF_NUMSYS__ = 60
    __HOUR__ = 0
    __MIN__ = 0
    __SEC__ = 0

    def __init__(self, name: str,
            hour: int=__HOUR__, min: int=__MIN__, sec: int=__SEC__):
        super().__init__(name)
        self._hour = assertion.is_int(hour)
        self._min = assertion.is_int(min)
        self._sec = assertion.is_int(sec)
        self._numsys = Time.__DEF_NUMSYS__

    @property
    def hour(self): return self._hour

    @property
    def min(self): return self._min

    @property
    def sec(self): return self._sec

    @property
    def numsys(self): return self._numsys

    def setNumsys(self, num: int):
        # NOTE: 最大値を100、最小を0にしておきます
        self._numsys = assertion.is_between(
                assertion.is_int(num), 100, 0)
        return self

    def inherited(self, name: str, hour: int=0, min: int=0, sec: int=0):
        return Time(name,
                self.hour + assertion.is_int(hour),
                self.min + assertion.is_int(min),
                self.sec + assertion.is_int(sec))
