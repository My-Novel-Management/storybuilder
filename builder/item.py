# -*- coding: utf-8 -*-
"""Define an item class.
"""
from . import assertion
from .basedata import BaseData


class Item(BaseData):
    """Data type of an item.
    """
    __NOTE__ = "なし"

    def __init__(self, name: str, note: str=__NOTE__, skin=None):
        """
        Args:
            name (str): an item name.
            note (str): a note.
        """
        super().__init__(name)
        self._note = assertion.is_str(note)
        from .skin import ItemSkin
        self._skin = skin if skin else ItemSkin(self)

    @property
    def note(self): return self._note

    @property
    def skin(self): return self._skin
