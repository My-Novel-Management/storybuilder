# -*- coding: utf-8 -*-
"""Define base data.
"""
## public libs
## local libs
from utils import assertion
from utils.util_id import UtilityID
## local files


class BaseData(object):
    """Base class for a data.
    """
    def __init__(self, name: str, data: tuple):
        self._data = assertion.isTuple(data)
        self._dataId = UtilityID.getNextId()
        self._name = assertion.isStr(name)

    @property
    def data(self) -> tuple:
        return self._data

    @property
    def dataId(self) -> int:
        return self._dataId

    @property
    def name(self) -> str:
        return self._name

