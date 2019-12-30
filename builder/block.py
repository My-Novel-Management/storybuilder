# -*- coding: utf-8 -*-
"""Define action container.
"""
## public libs
from __future__ import annotations
from typing import Tuple
## local libs
from utils import assertion
## local files
from builder import __PRIORITY_NORMAL__
from builder.action import Action
from builder.basecontainer import BaseContainer


class Block(BaseContainer):
    """The container class for actions. partial
    """
    def __init__(self, title: str, *args: Action, priority: int=__PRIORITY_NORMAL__, omit: bool=False):
        from utils.util_tools import tupleFiltered
        super().__init__(title,
                (assertion.isTuple(tupleFiltered(args, Action)),
                    ), priority=priority, omit=omit)

    ## property
    @property
    def acts(self) -> Tuple[Action, ...]:
        return self.data[0]

    ## methods
    def inherited(self, *args, title: str="") -> Block:
        return Block(title if title else self.title,
                *args,
                priority=self.priority)
