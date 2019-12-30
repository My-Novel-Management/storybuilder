# -*- coding: utf-8 -*-
"""Define data type of day
"""
## public libs
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
        super().__init__(name,
                (assertion.isInt(mon),
                    assertion.isInt(day),
                    assertion.isInt(year),
                    assertion.isStr(note),)
                )

    ## property
    @property
    def mon(self) -> int:
        return self.data[0]

    @property
    def day(self) -> int:
        return self.data[1]

    @property
    def year(self) -> int:
        return self.data[2]

    @property
    def note(self) -> str:
        return self.data[3]

