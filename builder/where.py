# -*- coding: utf-8 -*-
"""Define pronoun data for stage.
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Where(BaseData):
    """The data class for a pronoun.
    """
    __NAME__ = "__where__"
    def __init__(self):
        super().__init__(Where.__NAME__, ())

