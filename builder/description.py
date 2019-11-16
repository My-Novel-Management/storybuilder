# -*- coding: utf-8 -*-
"""Define description class.
"""
from enum import Enum
from . import assertion
from .basedata import BaseData


class DescType(Enum):
    """Description type.
    """
    DESC = "description"
    DIALOGUE = "dialogue"
    COMPLEX = "complex"


class Description(BaseData):
    """Data type of a description.
    """
    __NAME__ = "__desc__"
    def __init__(self, *args, desc_type: DescType=DescType.DESC):
        super().__init__(Description.__NAME__)
        self._descs = Description._validatedStrings(*args)
        self._desc_type = assertion.is_instance(desc_type, DescType)

    @property
    def descs(self): return self._descs

    @property
    def desc_type(self): return self._desc_type

    # privates
    def _validatedStrings(*args):
        return args if [assertion.is_str(v) for v in args] else ()


class NoDesc(Description):
    """Nothing data.
    """
    def __init__(self):
        super().__init__()
