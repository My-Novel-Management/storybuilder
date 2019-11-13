# -*- coding: utf-8 -*-
"""Define base subject class.
"""
from . import assertion
from .basedata import BaseData


class BaseSubject(BaseData):
    """Data type of a subject.
    """
    def __init__(self, name: str):
        super().__init__(name)


class NoSubject(BaseSubject):
    """Nothing data.
    """
    def __init__(self):
        super().__init__("__noone__")
