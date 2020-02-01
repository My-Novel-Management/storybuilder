# -*- coding: utf-8 -*-
"""Define actor class for writing
"""
## public libs
from __future__ import annotations
from typing import Any
## local libs
from utils import assertion
from utils.util_str import isAlphabetsOnly
## local files
from builder import __CONTINUED__
from builder import ActType, TagType, MetaType
from builder.action import Action
from builder.day import Day
from builder.item import Item
from builder.metadata import MetaData
from builder.person import Person
from builder.pronoun import Who
from builder.stage import Stage
from builder.time import Time
from builder.word import Word


## define type
AllSubjects = (Person, Stage, Day, Time, Item, Word, Who)


## define class
class Writer(object):
    """The actor class for writing
    """
    def __init__(self, src: AllSubjects):
        self._src = assertion.isInstance(src, AllSubjects)

    @property
    def src(self) -> AllSubjects:
        return self._src

    @classmethod
    def getWho(cls) -> Writer:
        return Writer(Who())

    @classmethod
    def continuedAct(cls, *args, **kwargs) -> Action:
        return Action(*args, act_type=ActType.META, tag_type=TagType.COMMAND, note=__CONTINUED__, **kwargs)

    ## method (basic)
    def do(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.ACT, **kwargs)

    def be(self, *args, **kwargs) -> Action:
        return Action(self.countSetIf(*args), *args, subject=self.src, act_type=ActType.BE, **kwargs)

    def destroy(self, *args, **kwargs) -> Action:
        return Action(self.countSetIf(*args), *args, subject=self.src, act_type=ActType.DESTROY, **kwargs)

    def have(self, *args, **kwargs) -> Action:
        return Action(self.countSetIf(*args), *args, subject=self.src, act_type=ActType.HAVE, **kwargs)

    def discard(self, *args, **kwargs) -> Action:
        return Action(self.countSetIf(*args), *args, subject=self.src, act_type=ActType.DISCARD, **kwargs)

    def come(self, *args, **kwargs) -> Action:
        return Action(self.countSetIf(*args), *args, subject=self.src, act_type=ActType.COME, **kwargs)

    def go(self, *args, **kwargs) -> Action:
        return Action(self.countSetIf(*args), *args, subject=self.src, act_type=ActType.GO, **kwargs)

    def hear(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.HEAR, **kwargs)

    def look(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.LOOK, **kwargs)

    def talk(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.TALK, **kwargs)

    def think(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.THINK, **kwargs)

    def explain(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.EXPLAIN, **kwargs)

    def voice(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.VOICE, **kwargs)

    def wear(self, *args, **kwargs) -> Action:
        return Action(*args, subject=self.src, act_type=ActType.WEAR, **kwargs)

    ## tag
    def br(self) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.BR)

    def comment(self, comment: str) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.COMMENT, note=comment)

    def hr(self) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.HR)

    def symbol(self, note: str) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.SYMBOL, note=note)

    def title(self, title: str) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.TITLE, note=title)

    ## meta
    def hasThat(self, *args, isScene: bool=False) -> Action:
        info = "scene" if isScene else ""
        return Action(MetaData(MetaType.TEST_HAS_THAT, note=info), *args,
                subject=self.src, act_type=ActType.META)

    def existsThat(self, *args, isScene: bool=False) -> Action:
        info = "scene" if isScene else ""
        return Action(MetaData(MetaType.TEST_EXISTS_THAT, note=info),
                *args, subject=self.src, act_type=ActType.META)

    ## methods (utility)
    @classmethod
    def countSetIf(cls, *args: Any) -> int:
        for v in args:
            if isinstance(v, int):
                return v
        else:
            return 1
