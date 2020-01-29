# -*- coding: utf-8 -*-
"""Define data type of day
"""
## public libs
import datetime
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Day(BaseData):
    """The data class of day.

    Attributes:
        name (str): a day name
        mon (int): 0. a month
        day (int): 1. a day
        year (int): 2. a year
        note (str): 3. a note
    """
    __YEAR__ = 2000
    __MON__ = 1
    __DAY__ = 1
    def __init__(self, name: str, mon: int=__MON__, day: int=__DAY__, year: int=__YEAR__, note: str=""):
        super().__init__(name, datetime.date(
                    year=assertion.isInt(year),
                    month=assertion.isInt(mon),
                    day=assertion.isInt(day),
                    ),
                note=note,
                )
    ## property
    @property
    def day(self) -> int:
        return self.data.day

    @property
    def mon(self) -> int:
        return self.data.month

    @property
    def year(self) -> int:
        return self.data.year

    ## methods
    def elapsedDay(self, val: int):
        return Day(self.name + f"・{val}日後",
                self.mon, self.day + val, self.year, note=self.note)

    def elapsedMonth(self, val: int):
        return Day(self.name + f"・{val}月後",
                self.mon + val, self.day, self.year, note=self.note)

    def elapsedYear(self, val: int):
        return Day(self.name + f"・{val}年後",
                self.mon, self.day, self.year + val, note=self.note)

    def nextDay(self):
        return Day(self.name + "・翌日",
                mon=self.mon, day=self.day + 1, year=self.year, note=self.note)

    def nextMonth(self):
        return Day(self.name + "・翌月",
                mon=self.mon + 1, day=self.day, year=self.year, note=self.note)

    def nextYear(self):
        return Day(self.name + "・翌年",
                mon=self.mon, day=self.day, year=self.year + 1, note=self.note)
