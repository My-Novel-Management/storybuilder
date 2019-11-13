# -*- coding: utf-8 -*-
"""Define a scene class.
"""
from enum import Enum
from . import assertion
from .basecontainer import BaseContainer
from .basedata import BaseData, NoData
from .person import Person
from .stage import Stage
from .day import Day
from .time import Time
from .action import Action


class ScenarioType(Enum):
    """Scenario element type.
    """
    TAG = "tag"
    TITLE = "title"
    PILLAR = "pillar"
    EFFECT = "effect"
    DIRECTION = "direction"
    DIALOGUE = "dialogue"
    # TODO: 脚本用の分類タグから

class Scene(BaseContainer):
    """The container for actions.
    """
    def __init__(self, title: str, outline: str, *args,
            camera: [Person, NoData]=None,
            stage: [Stage, NoData]=None,
            day: [Day, NoData]=None,
            time: [Time, NoData]=None):
        super().__init__(title, Action.DEF_PRIORITY)
        self._outline = assertion.is_str(outline)
        self._actions = Scene._validatedActions(*args)
        self._camera = assertion.is_instance(camera, Person) if camera else NoData()
        self._stage = assertion.is_instance(stage, Stage) if stage else NoData()
        self._day = assertion.is_instance(day, Day) if day else NoData()
        self._time = assertion.is_instance(time, Time) if time else NoData()

    def inherited(self, *acts):
        return Scene(self.title, self.outline,
                *acts,
                camera=self.camera, stage=self.stage, day=self.day, time=self.time) \
                .setPriority(self.priority)

    @property
    def actions(self): return self._actions

    @property
    def camera(self): return self._camera

    @property
    def day(self): return self._day

    @property
    def outline(self): return self._outline

    @property
    def stage(self): return self._stage

    @property
    def time(self): return self._time

    @property
    def title(self): return self._title

    def setCamera(self, camera: [Person, NoData]):
        """
        Args:
            XXX (:obj:`Chara`): a stage camera.
        """
        self._camera = camera if isinstance(camera, NoData) else assertion.is_instance(camera, Person)
        return self

    def setStage(self, stage: [Stage, NoData]):
        """
        Args:
            XXX (:obj:`Stage`): a stage of this scene.
        """
        self._stage = stage if isinstance(stage, NoData) else assertion.is_instance(stage, Stage)
        return self

    def setDay(self, day: [Day, NoData]):
        """
        Args:
            XXX (:obj:`Day`): a base day of this scene.
        """
        self._day = day if isinstance(day, NoData) else assertion.is_instance(day, Day)
        return self

    def setTime(self, time: [Time, NoData]):
        """
        Args:
            XXX (:obj:`Time`): a base time of this scene.
        """
        self._time = time if isinstance(time, NoData) else assertion.is_instance(time, Time)
        return self

    def add(self, *args):
        """
        Args:
            args (:obj:`Action`): scene actions.
        """
        self._actions = self._actions + Scene._validatedActions(*args)
        return self

    # privates
    def _validatedActions(*args):
        from .combaction import CombAction
        for a in args:
            if not isinstance(a, (Action, CombAction)):
                raise AssertionError("Must be data type of 'Action'!", a)
        return args

