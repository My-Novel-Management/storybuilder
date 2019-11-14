# -*- coding: utf-8 -*-
"""Define it class.
"""
from . import assertion
from .basedata import BaseData


class It(BaseData):
    """For a pronoun class.
    """
    __NAME__ = "__it__"

    def __init__(self):
        super().__init__(It.__NAME__)

