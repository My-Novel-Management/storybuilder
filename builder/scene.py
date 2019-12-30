# -*- coding: utf-8 -*-
"""Define action container.
"""
## public libs
from __future__ import annotations
from typing import Optional, Tuple
## local libs
from utils import assertion
## local files
from builder import __PRIORITY_NORMAL__
from builder.action import Action
from builder.basecontainer import BaseContainer
from builder.block import Block
from builder.day import Day
from builder.person import Person
from builder.stage import Stage
from builder.time import Time
from builder.when import When
from builder.where import Where
from builder.who import Who

## define types
PersonLike = (Person, Who)
StageLike = (Stage, Where)
DayLike = (Day, When)
TimeLike = (Time, When)


class Scene(BaseContainer):
    """The container class for actions.
    """
    def __init__(self, title: str, *args: Action,
            camera: Optional[Person]=None,
            stage: Optional[Stage]=None,
            day: Optional[Day]=None,
            time: Optional[Time]=None,
            note: str="", priority: int=__PRIORITY_NORMAL__, omit: bool=False):
        from utils.util_tools import tupleFiltered
        super().__init__(title,
                (assertion.isTuple(tupleFiltered(args, (Action, Block))),
                    assertion.isInstance(camera, PersonLike) if camera else Who(),
                    assertion.isInstance(stage, StageLike) if stage else Where(),
                    assertion.isInstance(day, DayLike) if day else When(),
                    assertion.isInstance(time, TimeLike) if time else When(),
                    assertion.isStr(note),
                ), priority=priority, omit=omit)

    ## property
    @property
    def actions(self) -> Tuple[Action, ...]:
        return self.data[0]

    @property
    def camera(self) -> PersonLike:
        return self.data[1]

    @property
    def stage(self) -> StageLike:
        return self.data[2]

    @property
    def day(self) -> DayLike:
        return self.data[3]

    @property
    def time(self) -> TimeLike:
        return self.data[4]

    @property
    def note(self) -> str:
        return self.data[5]

    ## methods
    def inherited(self, *args: Action, title: str="",
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
