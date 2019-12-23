# -*- coding: utf-8 -*-
"""Define description class.
"""
from enum import Enum, auto
from . import assertion
from .basedata import BaseData


class DescType(Enum):
    """Description type.
    """
    DESC = "description"
    DIALOGUE = "dialogue"
    COMPLEX = "complex"

class RubiType(Enum):
    """Rubi type.
    """
    NOSET = auto()
    ONCE = auto()
    EVERY = auto()


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

class Rubi(BaseData):
    """Data type of a rubi.
    """
    __NAME__ = "__rubi__"
    def __init__(self, base: str, rubi: str, exclusions: (str, list, tuple),
            rubi_type: RubiType=RubiType.ONCE):
        super().__init__(Rubi.__NAME__)
        self._base = assertion.is_str(base)
        self._rubi = Rubi._validatedRubi(rubi)
        self._rubi_type = assertion.is_instance(rubi_type, RubiType)
        self._exclusions = exclusions

    @property
    def base(self): return self._base

    @property
    def exclusions(self): return self._exclusions

    @property
    def rubi(self): return self._rubi

    @property
    def rubi_type(self): return self._rubi_type

    ## privates
    def _validatedRubi(val: str):
        if "《" in assertion.is_str(val) and "》" in val:
            return val
        else:
            raise AssertionError("Must be had 《》 in rubi: ", val)
