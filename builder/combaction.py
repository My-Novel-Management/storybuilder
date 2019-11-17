# -*- coding: utf-8 -*-
"""Define an action container class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .action import Action, TagAction
from . import __DEF_PRIORITY__


class CombAction(BaseContainer):
    """The container for actions.
    """
    __NAME__ = "__comb__"
    def __init__(self, *args):
        super().__init__(CombAction.__NAME__, __DEF_PRIORITY__)
        self._actions = CombAction._validatedActions(args)

    @property
    def actions(self): return self._actions

    def inherited(self, *args):
        return CombAction(*args).setPriority(self.priority)

    # privates
    def _validatedActions(args):
        return args if [assertion.is_instance(v, (Action, TagAction)) for v in args] else ()
