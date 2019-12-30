# -*- coding: utf-8 -*-
"""Define episode container.
"""
## public libs
from __future__ import annotations
from typing import Tuple
## local libs
from utils import assertion
## local files
from builder import __PRIORITY_NORMAL__
from builder.basecontainer import BaseContainer
from builder.episode import Episode


class Chapter(BaseContainer):
    """The container class for episodes.
    """
    def __init__(self, title: str, *args: Episode, note: str="", priority: int=__PRIORITY_NORMAL__, omit: bool=False):
        from utils.util_tools import tupleFiltered
        super().__init__(title,
                (assertion.isTuple(tupleFiltered(args, Episode)),
                    assertion.isStr(note),
                ), priority=priority, omit=omit)

    ## property
    @property
    def episodes(self) -> Tuple[Episode, ...]:
        return self.data[0]

    @property
    def note(self) -> str:
        return self.data[1]

    ## methods
    def inherited(self, *args: Episode, title: str="") -> Chapter:
        return Chapter(title if title else self.title,
                *args,
                note=self.note,
                priority=self.priority)
