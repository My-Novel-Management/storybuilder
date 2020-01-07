# -*- coding: utf-8 -*-
"""Define base container.
"""
## public libs
from __future__ import annotations
from typing import Any
## local libs
from utils import assertion
from utils.util_id import UtilityID
from utils.util_str import tupleEvenStr
## local files
from . import __PRIORITY_MIN__, __PRIORITY_MAX__, __PRIORITY_NORMAL__


class BaseContainer(object):
    """Base class for a container.
    """
    def __init__(self, title: str, *args: (str, list, tuple), note: str="", priority: int=__PRIORITY_NORMAL__):
        self._data = assertion.isTuple(tupleEvenStr(args))
        self._dataId = UtilityID.getNextId()
        self._note = assertion.isStr(note)
        self._priority = assertion.isBetween(priority, __PRIORITY_MAX__, __PRIORITY_MIN__)
        self._title = assertion.isStr(title)

    ## property
    @property
    def data(self) -> tuple:
        return self._data

    @property
    def dataId(self) -> int:
        return self._dataId

    @property
    def note(self) -> str:
        return self._note

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def title(self) -> str:
        return self._title

    ## common methods
    def isEqual(self, src: Any) -> bool:
        return isinstance(src, type(self)) and self.data == src.data

    def inherited(self, *args, **kwargs) -> BaseContainer:
        return BaseContainer(self.title, *args, note=self.note, priority=self.priority,
                **kwargs)

    def omit(self) -> BaseContainer:
        self._priority = __PRIORITY_MIN__
        return self
