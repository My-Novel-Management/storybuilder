# -*- coding: utf-8 -*-
"""Define day class.
"""
from . import assertion
from .basedata import BaseData


class Day(BaseData):
    """Data type of days.
    """
    DEF_YEAR = 2020
    DEF_MON = 1
    DEF_DAY = 1

    def __init__(self, name: str,
            mon: int=DEF_MON, day: int=DEF_DAY, year: int=DEF_YEAR):
        super().__init__(name)
        self._year = year
        self._mon = mon
        self._day = day

    @property
    def year(self): return self._year

    @property
    def mon(self): return self._mon

    @property
    def day(self): return self._day

