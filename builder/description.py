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
    def __init__(self, *args, desc_type: DescType=DescType.DESC):
        super().__init__("__desc__")
        self._descs = Description._validatedStrings(args)
        self._desc_type = assertion.is_instance(desc_type, DescType)

    @property
    def descs(self): return self._descs

    @property
    def desc_type(self): return self._desc_type

    # privates
    def _validatedStrings(args):
        if args:
            if isinstance(args, str):
                return (args,)
            else:
                return tuple(assertion.is_list(args))
        else:
            return ()


class NoDesc(Description):
    """Nothing data.
    """
    def __init__(self):
        super().__init__()
