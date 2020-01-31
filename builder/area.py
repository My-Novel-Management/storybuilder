# -*- coding: utf-8 -*-
"""Define data type of area
"""
## public libs
from __future__ import annotations
import math
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


## define class
class Area(BaseData):
    """The data class of stage.

    Attributes:
        name (str): a area name.
        x (int): a x point.
        y (int): a y point.
        note (str): a note.
    """
    def __init__(self, tag: str, name: str, x: int, y: int, note: str=""):
        super().__init__(name,
                (assertion.isInt(x), assertion.isInt(y),),
                note=note)
        self._tag = assertion.isStr(tag)

    ## statics
    @classmethod
    def getDefault(cls) -> Area:
        return Area("Zero", "中心", 0,0)

    ## property
    @property
    def tag(self) -> str:
        return self._tag

    @property
    def x(self) -> int:
        return self.data[0]

    @property
    def y(self) -> int:
        return self.data[1]

    ## methods
    def distance(self, val: Area) -> float:
        return math.hypot(self.x - val.x, self.y - val.y)
