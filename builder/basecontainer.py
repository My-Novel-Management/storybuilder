# -*- coding: utf-8 -*-
"""Define base container type class.
"""
from . import assertion
from . import __MAX_PRIORYTY__, __MIN_PRIORITY__


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
        self._priority = assertion.is_between(pri, __MAX_PRIORYTY__, __MIN_PRIORITY__)
        return self

    def omit(self):
        self._priority = __MIN_PRIORITY__
        return self

