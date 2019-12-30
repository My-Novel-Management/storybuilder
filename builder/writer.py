# -*- coding: utf-8 -*-
"""Define actor class for writing
"""
## public libs
from __future__ import annotations
## local libs
from utils import assertion
from utils.util_str import isAlphabetsOnly
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.baseactor import BaseActor
from builder.day import Day
from builder.item import Item
from builder.person import Person
from builder.shot import Shot
from builder.stage import Stage
from builder.time import Time
from builder.who import Who


## type defines
AllDataType = (Day, Item, Person, Stage, Time, Who)


class Writer(BaseActor):
    """The actor class for writing
    """
    def __init__(self, src: AllDataType,
            ):
        super().__init__(assertion.isInstance(src, AllDataType))

    @classmethod
    def getWho(cls) -> Writer:
        return Writer(Who())

    ## act
    def be(self, *args, **kwargs) -> Action:
        return Action("be",
                *args, subject=self.src, act_type=ActType.BE,
                note=self._countIf(args), **kwargs)

    def come(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "come"),
                *args, subject=self.src, act_type=ActType.COME,
                note="1", **kwargs)

    def destroy(self, *args, **kwargs) -> Action:
        return Action("destroy",
                *args, subject=self.src, act_type=ActType.DESTROY,
                note=self._countIf(args), **kwargs)

    def discard(self, *args, **kwargs) -> Action:
        return Action("discard",
                *args, subject=self.src, act_type=ActType.DISCARD,
                note=self._countIf(args), **kwargs)

    def do(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "do"),
                *args, subject=self.src, act_type=ActType.ACT, **kwargs)

    def explain(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "explain"),
                *args, subject=self.src, act_type=ActType.EXPLAIN, **kwargs)

    def go(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "go"),
                *args, subject=self.src, act_type=ActType.GO,
                note="1", **kwargs)

    def have(self, *args, **kwargs) -> Action:
        return Action("have",
                *args, subject=self.src, act_type=ActType.HAVE,
                note=self._countIf(args), **kwargs)

    def hear(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "hear"),
                *args, subject=self.src, act_type=ActType.HEAR, **kwargs)

    def look(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "look"),
                *args, subject=self.src, act_type=ActType.LOOK, **kwargs)

    def move(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "move"),
                *args, subject=self.src, act_type=ActType.MOVE, **kwargs)

    def takeoff(self, *args, **kwargs) -> Action:
        return Action("takeoff",
                *args, subject=self.src, act_type=ActType.TAKEOFF,
                note=self._countIf(args), **kwargs)

    def talk(self, *args, **kwargs) -> Action:
        return Action("talk",
                Shot(*args, isTerm=True), subject=self.src, act_type=ActType.TALK, **kwargs)

    def talking(self, *args, **kwargs) -> Action:
        return Action("talk",
                Shot(*args), subject=self.src, act_type=ActType.TALK, **kwargs)

    def think(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "think"),
                *args, subject=self.src, act_type=ActType.THINK, **kwargs)

    def wear(self, *args, **kwargs) -> Action:
        return Action("wear",
                *args, subject=self.src, act_type=ActType.WEAR,
                note=self._countIf(args), **kwargs)
    ## hook
    def feel(self, *args, **kwargs) -> Action:
        return Action(self._doingIf(args, "feel"),
                *args, subject=self.src, act_type=ActType.THINK, **kwargs)

    ## tag
    def br(self, num: (int, str)=1) -> Action:
        return Action("tag", act_type=ActType.TAG, tag_type=TagType.BR, note=str(num))

    def comment(self, comment: str) -> Action:
        return Action("tag", act_type=ActType.TAG, tag_type=TagType.COMMENT, note=comment)

    def hr(self) -> Action:
        return Action("tag", act_type=ActType.TAG, tag_type=TagType.HR)

    def symbol(self, note: str) -> Action:
        return Action("tag", act_type=ActType.TAG, tag_type=TagType.SYMBOL, note=note)

    def title(self, title: str) -> Action:
        return Action("tag", act_type=ActType.TAG, tag_type=TagType.TITLE, note=title)

    ## privates
    def _doingIf(self, args: tuple, doing: str) -> str:
        return args[0] if args and isAlphabetsOnly(args[0]) else doing

    def _countIf(self, args: tuple) -> str:
        return str(args[0]) if args and isinstance(args[0], int) else "1"
