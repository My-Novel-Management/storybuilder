# -*- coding: utf-8 -*-
"""Define base container.
"""
## public libs
from __future__ import annotations
## local libs
from utils import assertion
from utils.util_id import UtilityID
## local files
from . import __PRIORITY_MIN__, __PRIORITY_NORMAL__


class BaseContainer(object):
    """Base class for a container.
    """
    def __init__(self, title: str, data: tuple, priority: int=__PRIORITY_NORMAL__, omit: bool=False):
        self._data = assertion.isTuple(data)
        self._dataId = UtilityID.getNextId()
        self._priority = __PRIORITY_MIN__ if omit else priority
        self._title = assertion.isStr(title)

    ## property
    @property
    def data(self) -> tuple:
        return self._data

    @property
    def dataId(self) -> int:
        return self._dataId

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def title(self) -> str:
        return self._title

    ## common methods
    def inherited(self, *args, **kwargs) -> BaseContainer:
        return BaseContainer(self.title,
                data=args if args else self.data,
                priority=self.priority, **kwargs)

