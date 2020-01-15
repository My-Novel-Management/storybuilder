# -*- coding: utf-8 -*-
"""Define action container for sub note.
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
from builder.person import Person


## define class
class LifeNote(BaseContainer):
    """The container class for actions. partial
    """
    def __init__(self, title: str, subject: Person, *args: Action,
            note: str="", priority: int=__PRIORITY_NORMAL__):
        super().__init__(title,
                assertion.isTuple(tupleFiltered(args, Action)),
                note=note,
                priority=priority)
        self._subject = assertion.isInstance(subject, Person)

    ## property
    @property
    def subject(self) -> Person:
        return self._subject

    ## methods
    def inherited(self, *args, title: str="", note: str=None) -> LifeNote:
        return LifeNote(title if title else self.title,
                self.subject,
                *args,
                note=note if note else self.note,
                priority=self.priority)
