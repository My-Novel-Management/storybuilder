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
        name (str): a name
        note (str): a note
    """
    def __init__(self, data_type: MetaType=MetaType.INFO, title: str="", note: str=""):
        super().__init__(title,
                assertion.isInstance(data_type, MetaType), note=note)

