# -*- coding: utf-8 -*-
"""Define action container.
"""
## public libs
from __future__ import annotations
from typing import Optional, Tuple
## local libs
from utils import assertion
from utils.util_str import tupleFiltered
## local files
from builder import __PRIORITY_NORMAL__
from builder.action import Action
from builder.basecontainer import BaseContainer
from builder.block import Block
from builder.day import Day
from builder.person import Person
from builder.pronoun import When, Where, Who
from builder.stage import Stage
from builder.time import Time


## define types
ActionLike = (Action, Block)
PersonLike = (Person, Who)
StageLike = (Stage, Where)
DayLike = (Day, When)
TimeLike = (Time, When)


## define class
class Scene(BaseContainer):
    """The container class for actions.
    """
    def __init__(self, title: str, *args: ActionLike,
            camera: Optional[Person]=None,
            stage: Optional[Stage]=None,
            day: Optional[Day]=None,
            time: Optional[Time]=None,
            note: str="", priority: int=__PRIORITY_NORMAL__):
        super().__init__(title, assertion.isTuple(tupleFiltered(args, ActionLike)),
                note=note,
                priority=priority)
        self._camera = assertion.isInstance(camera, PersonLike) if camera else Who()
        self._stage = assertion.isInstance(stage, StageLike) if stage else Where()
        self._day = assertion.isInstance(day, DayLike) if day else When()
        self._time = assertion.isInstance(time, TimeLike) if time else When()

    ## property
    @property
    def camera(self) -> PersonLike:
        return self._camera

    @property
    def stage(self) -> StageLike:
        return self._stage

    @property
    def day(self) -> DayLike:
        return self._day

    @property
    def time(self) -> TimeLike:
        return self._time

    ## methods
    def inherited(self, *args: ActionLike, title: str="",
            camera: Optional[Person]=None,
            stage: Optional[Stage]=None,
            day: Optional[Day]=None,
            time: Optional[Time]=None,
            ) -> Scene:
        return Scene(title if title else self.title,
                *args,
                camera=camera if camera else self.camera,
                stage=stage if stage else self.stage,
                day=day if day else self.day,
                time=time if time else self.time,
                note=self.note,
                priority=self.priority)
