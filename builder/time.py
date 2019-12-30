# -*- coding: utf-8 -*-
"""Define data type of time
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Time(BaseData):
    """The data class of time.

    Attributes:
        name (str): a time name
        hour (int): 0. an hour
        min (int): 1. a minute
        sec (int): 2. a second
        note (str): 3. a note
    """
    __HOUR__ = 10
    __MIN__ = 0
    __SEC__ = 0
    def __init__(self, name: str, hour: int=__HOUR__, min: int=__MIN__, sec: int=__SEC__, note: str=""):
        super().__init__(name,
                (assertion.isInt(hour),
                    assertion.isInt(min),
                    assertion.isInt(sec),
                    assertion.isStr(note),
                    ))

    ## property
    @property
    def hour(self) -> int:
        return self.data[0]

    @property
    def min(self) -> int:
        return self.data[1]

    @property
    def sec(self) -> int:
        return self.data[2]

    @property
    def note(self) -> str:
        return self.data[3]
