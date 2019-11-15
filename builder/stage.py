# -*- coding: utf-8 -*-
"""Define stage class.
"""
from . import assertion
from .basedata import BaseData
from .item import Item


class Stage(BaseData):
    """Data type of a stage.
    """
    __NOTE__ = "nothing"
    def __init__(self, name: str, note: str=__NOTE__):
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

    def inherited(self, name: str, note: str=None):
        # TODO: parent and child
        return Stage(
                name if name != self.name else self.name,
                note if note and note != self.note else self.note)

    # privates
    def _validatedItems(*args):
        return args if [assertion.is_instance(v, Item) for v in args] else ()

