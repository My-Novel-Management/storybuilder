# -*- coding: utf-8 -*-
"""Define scene container.
"""
## public libs
from __future__ import annotations
from typing import Tuple
## local libs
from utils import assertion
## local files
from builder import __PRIORITY_NORMAL__
from builder.basecontainer import BaseContainer
from builder.scene import Scene


class Episode(BaseContainer):
    """The container class for scenes.

    Attributes:
        title (str): a episode title
        scenes (tuple:Scene): 0. scenes
        note (str): 1. a note
    """
    def __init__(self, title: str, *args: Scene, note: str="", priority: int=__PRIORITY_NORMAL__, omit: bool=False):
        from utils.util_tools import tupleFiltered
        super().__init__(title,
                (assertion.isTuple(tupleFiltered(args, Scene)),
                    assertion.isStr(note),
                ), priority=priority, omit=omit)

    ## property
    @property
    def scenes(self) -> Tuple[Scene, ...]:
        return self.data[0]

    @property
    def note(self) -> str:
        return self.data[1]

    ## methods
    def inherited(self, *args: Scene, title: str="") -> Episode:
        return Episode(title if title else self.title,
                *args,
                note=self.note,
                priority=self.priority)
