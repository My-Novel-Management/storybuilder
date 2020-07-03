# -*- coding: utf-8 -*-
'''
Scene Information Data
======================
'''

from __future__ import annotations

__all__ = ('SceneInfo',)


import datetime
from builder.objects.day import Day
from builder.objects.time import Time
from builder.objects.person import Person
from builder.objects.stage import Stage
from builder.utils import assertion


class SceneInfo(object):
    ''' Scene Info Data class.
    '''
    def __init__(self,
            camera: Person,
            stage: Stage,
            day: Day,
            time: Time,
            persons: (list, tuple),
            ):
        self._camera = assertion.is_instance(camera, Person) if camera else None
        self._stage = assertion.is_instance(stage, Stage) if stage else None
        self._day = assertion.is_instance(day, Day) if day else None
        self._time = assertion.is_instance(time, Time) if time else None
        self._persons = assertion.is_listlike(persons) if persons else ()

    #
    # property
    #

    @property
    def camera(self) -> (Person, None):
        return self._camera

    @property
    def stage(self) -> (Stage, None):
        return self._stage

    @property
    def day(self) -> (Day, None):
        return self._day

    @property
    def time(self) -> (Time, None):
        return self._time

    @property
    def persons(self) -> (list, tuple):
        return self._persons

