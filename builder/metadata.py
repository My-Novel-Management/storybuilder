# -*- coding: utf-8 -*-
"""Define data type for meta info
"""
## public libs
## local libs
from utils import assertion
## local files
from builder import MetaType
from builder.basedata import BaseData


## define class
class MetaData(BaseData):
    """The data class of meta data

    Attributes:
        name (str): a item name
        note (str): 0. a note
    """
    __NAME__ = "__meta__"
    def __init__(self, data_type: MetaType=MetaType.INFO, info: str=""):
        super().__init__(MetaData.__NAME__,
                assertion.isInstance(data_type, MetaType), note=info)

