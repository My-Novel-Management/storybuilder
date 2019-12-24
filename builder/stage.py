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
    def __init__(self, name: str, note: str=__NOTE__, skin=None):
        super().__init__(name)
        self._note = assertion.is_str(note)
        self._items = ()
        from .skin import StageSkin
        self._skin = skin if skin else StageSkin(self)

    @property
    def items(self): return self._items

    @property
    def note(self): return self._note

    @property
    def skin(self): return self._skin

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
                note if note and note != self.note else self.note,
                skin=self.skin)

    # privates
    def _validatedItems(*args):
        return args if [assertion.is_instance(v, Item) for v in args] else ()

