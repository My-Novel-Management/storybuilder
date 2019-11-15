# -*- coding: utf-8 -*-
"""Define word class.
"""
from . import assertion
from .basedata import BaseData


class Word(BaseData):
    """Data type of a word.
    """
    __NOTE__ = "nothing"

    def __init__(self, name: str, note: str=__NOTE__):
        super().__init__(name)
        self._note = assertion.is_str(note)

    @property
    def note(self): return self._note

