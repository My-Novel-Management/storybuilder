# -*- coding: utf-8 -*-
"""Define action container.
"""
## public libs
from __future__ import annotations
from typing import Tuple
## local libs
from utils import assertion
from utils.util_str import tupleFiltered
## local files
from builder import __PRIORITY_NORMAL__
from builder.action import Action
from builder.basecontainer import BaseContainer


## define class
class Block(BaseContainer):
    """The container class for actions. partial
    """
    def __init__(self, title: str, *args: Action, note: str="", priority: int=__PRIORITY_NORMAL__):
        super().__init__(title,
                assertion.isTuple(tupleFiltered(args, Action)),
                note=note,
                priority=priority)

    ## methods
    def inherited(self, *args, title: str="") -> Block:
        return Block(title if title else self.title,
                *args,
                note=self.note,
                priority=self.priority)
