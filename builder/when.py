# -*- coding: utf-8 -*-
"""Define pronoun data for day and time.
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class When(BaseData):
    """The data class for a pronoun.
    """
    __NAME__ = "__when__"
    def __init__(self):
        super().__init__(When.__NAME__, ())

