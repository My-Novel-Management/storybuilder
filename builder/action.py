# -*- coding: utf-8 -*-
"""Define container for action objects.
"""
## public libs
from __future__ import annotations
from typing import Any, Union, Tuple
## local libs
from utils import assertion
## local files
from builder import __PRIORITY_NORMAL__
from builder import ActType, TagType
from builder.basecontainer import BaseContainer
from builder.day import Day
from builder.item import Item
from builder.person import Person
from builder.shot import Shot
from builder.stage import Stage
from builder.time import Time
from builder.who import Who
from builder.word import Word


## define types
AllSubjects = (Person, Day, Item, Stage, Time, Who)


class Action(BaseContainer):
    """The container class for an action.

    Attributes:
        acts (tuple:Any): actions
        subject (Person): a subject
    """
    __TITLE__ = "__action__"
    def __init__(self, doing: str, *args: Any, subject: AllSubjects=None,
            act_type: ActType=ActType.ACT,
            tag_type: TagType=TagType.NONE,
            note: str="", priority: int=__PRIORITY_NORMAL__, omit: bool=False):
        from utils.util_tools import tupleFiltered
        super().__init__(Action.__TITLE__,
                (
                    assertion.isTuple(tupleFiltered(args, (str, Shot, Person, Item, Day, Stage, Time, Word))),
                    assertion.isStr(doing),
                    assertion.isInstance(subject, AllSubjects) if subject else Who(),
                    assertion.isInstance(act_type, ActType),
                    assertion.isInstance(tag_type, TagType),
                    assertion.isStr(note),
                ), priority=priority, omit=omit)

    ## property
    @property
    def acts(self) -> Tuple[Union[str, Shot], ...]:
        return self.data[0]

    @property
    def doing(self) -> str:
        return self.data[1]

    @property
    def subject(self) -> AllSubjects:
        return self.data[2]

    @property
    def act_type(self) -> ActType:
        return self.data[3]

    @property
    def tag_type(self) -> TagType:
        return self.data[4]

    @property
    def note(self) -> str:
        return self.data[5]

    ## methods
    def inherited(self, *args: Any, subject: AllSubjects=None, note: str="") -> Action:
        return Action(self.doing,
                *args,
                subject=subject if subject else self.subject,
                act_type=self.act_type,
                tag_type=self.tag_type,
                note=note if note else self.note,
                priority=self.priority)
