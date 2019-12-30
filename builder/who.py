# -*- coding: utf-8 -*-
"""Define pronoun data for person.
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Who(BaseData):
    """The data class for a pronoun.
    """
    __NAME__ = "__who__"
    def __init__(self):
        super().__init__(Who.__NAME__, ())

