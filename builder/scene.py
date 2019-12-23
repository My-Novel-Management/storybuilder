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
from .action import Action, TagAction
from .combaction import CombAction
from .basesubject import NoSubject
from .who import Who, When, Where
from . import __DEF_PRIORITY__


## type define
AllActions = (Action, TagAction, CombAction)
Someone = (Person, NoSubject)


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
    __nextid__ = 1

    def __init__(self, title: str, outline: str, *args,
            camera: (Person, NoData, Who)=None,
            stage: (Stage, NoData, Where)=None,
            day: (Day, NoData, When)=None,
            time: (Time, NoData, When)=None,
            inheritedId: int=0):
        super().__init__(title, __DEF_PRIORITY__)
        self._outline = assertion.is_str(outline)
        self._actions = Scene._validatedActions(*args)
        self._camera = Scene._validatedCamera(camera)
        self._stage = Scene._validatedStage(stage)
        self._day = Scene._validatedDay(day)
        self._time = Scene._validatedTime(time)
        self._sceneId = inheritedId if inheritedId else Scene._nextId()

    def inherited(self, *acts,
            title: str=None,
            outline: str=None,
            camera=None, stage=None, day=None, time=None):
        return Scene(self.title if not title else assertion.is_str(title),
                self.outline if not outline else assertion.is_str(outline),
                *acts,
                camera=camera if camera else self.camera,
                stage=stage if stage else self.stage,
                day=day if day else self.day,
                time=time if time else self.time,
                inheritedId=self.sceneId
                ).setPriority(self.priority)

    @property
    def sceneId(self): return self._sceneId

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

    def setCamera(self, camera: [Someone, NoData]):
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
    def _nextId() -> int:
        tmp = Scene.__nextid__
        Scene.__nextid__ += 1
        return tmp

    def _validatedActions(*args):
        return args if [assertion.is_instance(v, AllActions) for v in args] else ()

    def _validatedCamera(camera: (Person, NoSubject, NoData, Who)):
        return camera if isinstance(camera, (Person, Who)) else Who()

    def _validatedStage(stage: (Stage, NoData, Where)):
        return stage if isinstance(stage, (Stage, Where)) else Where()

    def _validatedDay(day: (Day, NoData, When)):
        return day if isinstance(day, (Day, When)) else When()

    def _validatedTime(time: (Time, NoData, When)):
        return time if isinstance(time, (Time, When)) else When()

