# -*- coding: utf-8 -*-
"""Define data type of time
"""
## public libs
import datetime
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


## define class
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
                datetime.time(
                    hour=assertion.isInt(hour),
                    minute=assertion.isInt(min),
                    second=assertion.isInt(sec),
                    ),
                note=note,
                )

