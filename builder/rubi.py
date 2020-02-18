# -*- coding: utf-8 -*-
"""Define data type of rubi
"""
## public libs
## local libs
from utils import assertion
from utils.util_str import tupleEvenStr
## local files
from builder.basedata import BaseData


class Rubi(BaseData):
    """The data class of rubi.

    Attributes:
        name (str): 0. a base word
        rubi (str): 1. a rubi word
        exclusions (tuple): 2. exclusion words
        isAlways (bool): True or False
    """
    def __init__(self, name: str, rubi: str, exclusions: (str, list, tuple)="",
            isAlways: bool=False):
        super().__init__(name, assertion.isStr(rubi))
        self._exclusions = assertion.isTuple(tupleEvenStr(exclusions))
        self._isAlways = assertion.isBool(True if isAlways else False)

    ## property
    @property
    def exclusions(self) -> tuple:
        return self._exclusions

    @property
    def isAlways(self) -> bool:
        return self._isAlways
