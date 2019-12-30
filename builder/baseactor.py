# -*- coding: utf-8 -*-
"""Define base actor.
"""
## public libs
## local libs
from utils import assertion
from utils.util_id import UtilityID
## local files
from builder.basedata import BaseData


class BaseActor(object):
    """Base class for a data.
    """
    def __init__(self, src: BaseData):
        self._actId = UtilityID.getNextId()
        self._src = assertion.isInstance(src, BaseData)

    @property
    def actId(self) -> int:
        return self._actId

    @property
    def src(self) -> BaseData:
        return self._src
