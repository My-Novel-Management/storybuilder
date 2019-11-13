# -*- coding: utf-8 -*-
"""Define stage class.
"""
from . import assertion
from .basedata import BaseData
from .item import Item


class Stage(BaseData):
    """Data type of a stage.
    """
    def __init__(self, name: str, note: str="nothing"):
        super().__init__(name)
        self._note = assertion.is_str(note)
        self._items = ()

    @property
    def items(self): return self._items

    @property
    def note(self): return self._note

    def add(self, *args):
        """
        Args:
            args (:obj:`Item`): a item object.
        """
        self._items = self._items + Stage._validatedItems(*args)
        return self

    # privates
    def _validatedItems(*args):
        for a in args:
            if not isinstance(a, Item):
                raise AssertionError("Must be data type 'Item'!")
        return args

