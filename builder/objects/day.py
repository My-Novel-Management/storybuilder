# -*- coding: utf-8 -*-
'''
Day Object
==========
'''

from __future__ import annotations

__all__ = ('Day',)


import datetime
from builder.objects.sobject import SObject
from builder.utils import assertion


class Day(SObject):
    ''' Day Object class.
    '''

    def __init__(self, name: str, month: int=1, day: int=1, year: int=2020, info: str=''):
        super().__init__(name)
        self._date = datetime.date(
                month=assertion.is_int(month),
                day=assertion.is_int(day),
                year=assertion.is_int(year))
        self._info = assertion.is_str(info)

    #
    # property
    #

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def daystring(self) -> str:
        return f'{self.month}月{self.day}日／{self.year}年'

    @property
    def month(self) -> int:
        return self._date.month

    @property
    def day(self) -> int:
        return self._date.day

    @property
    def year(self) -> int:
        return self._date.year

    @property
    def info(self) -> str:
        return self._info

    #
    # methods
    #

