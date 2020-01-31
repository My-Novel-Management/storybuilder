# -*- coding: utf-8 -*-
"""Define container for action objects.
"""
## public libs
from __future__ import annotations
from typing import Any, Union, Tuple
## local libs
from utils import assertion
from utils.util_str import tupleEvenStr
## local files
from builder import __PRIORITY_NORMAL__
from builder import ActType, TagType, MetaType
from builder.basecontainer import BaseContainer
from builder.conjuction import Then
from builder.day import Day
from builder.item import Item
from builder.metadata import MetaData
from builder.person import Person
from builder.stage import Stage
from builder.time import Time
from builder.word import Word
from builder.pronoun import Who


## define types
AllSubjects = (Person, Stage, Day, Time, Item, Word, Who)


## define class
class Action(BaseContainer):
    """The container class for an action.

    Attributes:
        acts (tuple:Any): actions
        subject (Person): a subject
    """
    __TITLE__ = "__action__"
    def __init__(self, *args: Any, subject: AllSubjects=Who(),
            act_type: ActType=ActType.ACT,
            tag_type: TagType=TagType.NONE,
            itemCount: int=0,
            note: str="", priority: int=__PRIORITY_NORMAL__):
        super().__init__(Action.__TITLE__,
                Action.argsReplaced(*args),
                note=note,
                priority=priority)
        self._act_type = assertion.isInstance(act_type, ActType)
        self._subject = assertion.isInstance(subject, AllSubjects)
        self._tag_type = assertion.isInstance(tag_type, TagType)
        self._itemCount = itemCount if itemCount else self.countIf(*args)

    ## property
    @property
    def subject(self) -> AllSubjects:
        return self._subject

    @property
    def act_type(self) -> ActType:
        return self._act_type

    @property
    def tag_type(self) -> TagType:
        return self._tag_type

    @property
    def itemCount(self) -> int:
        return self._itemCount

    ## methods
    def inherited(self, *args: Any, subject=None, note: str=None) -> Action:
        return Action(*args,
                subject=subject if subject else self.subject,
                act_type=self.act_type,
                tag_type=self.tag_type,
                itemCount=self.itemCount,
                note=note if note else self.note,
                priority=self.priority)

    @classmethod
    def argsReplaced(cls, *args: Any) -> tuple:
        tmp = []
        for v in args:
            if isinstance(v, str):
                if "&" == v:
                    tmp.append(Then())
                elif v.startswith('#'):
                    ## NOTE: current info only
                    tmp.append(MetaData(MetaType.INFO, note=v.replace('#', '＃', 1)))
                else:
                    tmp.append(v)
            elif isinstance(v, AllSubjects):
                tmp.append(v)
            elif isinstance(v, MetaData):
                tmp.append(v)
            elif isinstance(v, Then):
                tmp.append(v)
        return tuple(tmp)

    @classmethod
    def countIf(cls, *args: Any) -> int:
        for v in args:
            if isinstance(v, int):
                return v
        return 0
