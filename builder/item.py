# -*- coding: utf-8 -*-
"""Define an item class.
"""
from . import assertion
from .basedata import BaseData


class Item(BaseData):
    """Data type of an item.
    """
    __NOTE__ = "なし"

    def __init__(self, name: str, note: str=__NOTE__):
        """
        Args:
            name (str): an item name.
            note (str): a note.
        """
        super().__init__(name)
        self._note = assertion.is_str(note)

    @property
    def note(self): return self._note
