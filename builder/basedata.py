# -*- coding: utf-8 -*-
"""Define base data type class.
"""
from . import assertion


class BaseData(object):
    """Base class for data type.
    """
    def __init__(self, name: str):
        self._name = assertion.is_str(name)

    @property
    def name(self): return self._name


class NoData(BaseData):
    """Nothing data.
    """
    def __init__(self):
        super().__init__("__none__")

