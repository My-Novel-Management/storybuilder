# -*- coding: utf-8 -*-
"""Define base data.
"""
## public libs
from typing import Any
## local libs
from utils import assertion
from utils.util_id import UtilityID
## local files


class BaseData(object):
    """Base class for a data.
    """
    def __init__(self, name: str, *args: Any, note: str=""):
        self._data = args if args and len(args) > 1 else (args[0] if args else None)
        self._dataId = UtilityID.getNextId()
        self._name = assertion.isStr(name)
        self._note = assertion.isStr(note)
        self._textures = {}

    @property
    def data(self) -> Any:
        return self._data

    @property
    def dataId(self) -> int:
        return self._dataId

    @property
    def name(self) -> str:
        return self._name

    @property
    def note(self) -> str:
        return self._note

    @property
    def textures(self) -> dict:
        return self._textures

    ## methods (setter)
    def setTexture(self, key: str, val: str):
        self._textures[assertion.isStr(key)] = assertion.isStr(val)

    def updateTextures(self, vals: dict):
        self._textures.update(assertion.isDict(vals))
