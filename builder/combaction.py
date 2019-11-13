# -*- coding: utf-8 -*-
"""Define an action container class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .action import Action


class CombAction(BaseContainer):
    """The container for actions.
    """
    def __init__(self, *args):
        super().__init__("__comb__", Action.DEF_PRIORITY)
        self._actions = CombAction._validatedActions(*args)

    @property
    def actions(self): return self._actions

    def inherited(self, *args):
        return CombAction(*args).setPriority(self.priority)

    # privates
    def _validatedActions(*args):
        for a in args:
            if not isinstance(a, Action):
                raise AssertionError("Must be data type of 'Action'!")
        return args
