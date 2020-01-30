# -*- coding: utf-8 -*-
"""Define data type of stage
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


## define class
class Stage(BaseData):
    """The data class of stage.

    Attributes:
        name (str): a stage name.
        note (str): 0. a note.
    """
    def __init__(self, name: str, area: str="", info: str="", note: str=""):
        super().__init__(name,
                (assertion.isStr(area), assertion.isStr(info),),
                note=note)

    ## property
    @property
    def area(self) -> str:
        return self.data[0]

    @property
    def info(self) -> str:
        return self.data[1]
