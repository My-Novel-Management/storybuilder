# -*- coding: utf-8 -*-
"""Define day class.
"""
from . import assertion
from .basedata import BaseData


class Day(BaseData):
    """Data type of days.
    """
    __YEAR__ = 2020
    __MON__ = 1
    __DAY__ = 1

    def __init__(self, name: str,
            mon: int=__MON__, day: int=__DAY__, year: int=__YEAR__):
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

    def inherited(self, name: str="", mon: int=0, day: int=0, year: int=0):
        return Day(
                name if assertion.is_str(name) else self.name,
                self.mon + mon if assertion.is_int(mon) != 0 else self.mon,
                self.day + day if assertion.is_int(day) != 0 else self.day,
                self.year + year if assertion.is_int(year) != 0 else self.year)
