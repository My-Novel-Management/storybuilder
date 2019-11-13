# -*- coding: utf-8 -*-
"""Define base container type class.
"""
from . import assertion


class BaseContainer(object):
    """Base class for a container.
    """
    def __init__(self, title: str, priority: int):
        self._title = assertion.is_str(title)
        self._priority = assertion.is_int(priority)

    @property
    def title(self): return self._title

    @property
    def priority(self): return self._priority

    def setPriority(self, pri: int):
        # TODO: min max check
        self._priority = pri
        return self

    def omit(self):
        from .action import Action
        self._priority = Action.MIN_PRIORITY
        return self

