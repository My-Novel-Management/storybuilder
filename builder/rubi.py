# -*- coding: utf-8 -*-
"""Define data type of rubi
"""
## public libs
## local libs
from utils import assertion
from utils import util_tools as util
## local files
from builder.basedata import BaseData


class Rubi(BaseData):
    """The data class of rubi.

    Attributes:
        name (str): 0. a base word
        rubi (str): 1. a rubi word
        exclusions (tuple): 2. exclusion words
    """
    def __init__(self, name: str, rubi: str, exclusions: (str, list, tuple)="",
            isAlways: bool=False):
        super().__init__(name,
                (assertion.isStr(rubi),
                    assertion.isTuple(util.tupleEvenStr(exclusions)),
                    assertion.isBool(True if isAlways else False),
                    ))

    ## property
    @property
    def rubi(self) -> str:
        return self.data[0]

    @property
    def exclusions(self) -> tuple:
        return self.data[1]

    @property
    def isAlways(self) -> bool:
        return self.data[2]
