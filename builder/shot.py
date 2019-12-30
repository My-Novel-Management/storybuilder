# -*- coding: utf-8 -*-
"""Define data type of shot
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Shot(BaseData):
    """The data class of shot.

    Attributes:
        infos (tuple): 0. a info
    """
    __NAME__ = "__shot__"
    def __init__(self, *args: str, isTerm: bool=False):
        from utils.util_tools import tupleFiltered
        super().__init__(Shot.__NAME__,
                (assertion.isTuple(tupleFiltered(args, str)),
                    assertion.isBool(isTerm),
                    ))

    ## property
    @property
    def infos(self) -> tuple:
        return self.data[0]

    @property
    def isTerm(self) -> bool:
        return self.data[1]
