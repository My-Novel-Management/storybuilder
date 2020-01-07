# -*- coding: utf-8 -*-
"""Define special data type for action joint
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Then(BaseData):
    """The conjuction for action.
    """
    __NAME__ = "__then__"
    def __init__(self):
        super().__init__(Then.__NAME__, None)

