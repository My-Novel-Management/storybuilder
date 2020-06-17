# -*- coding: utf-8 -*-
'''
Time Object
===========
'''

from __future__ import annotations

__all__ = ('Time',)


import datetime
from builder.objects.sobject import SObject
from builder.utils import assertion


class Time(SObject):
    ''' Time Object class.
    '''

    def __init__(self, name: str, hour: int, minute: int):
        super().__init__(name)
        self._time = datetime.time(
                hour=assertion.is_int(hour),
                minute=assertion.is_int(minute))

    #
    # property
    #

    @property
    def time(self) -> datetime.time:
        return self._time

    @property
    def hour(self) -> int:
        return self._time.hour

    @property
    def minute(self) -> int:
        return self._time.minute

    #
    # methods
    #

