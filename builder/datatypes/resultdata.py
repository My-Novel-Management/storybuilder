# -*- coding: utf-8 -*-
'''
Result Data Object
==================
'''

from __future__ import annotations

__all__ = ('ResultData',)


from builder.containers.container import Container
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.rawdata import RawData
from builder.utils import assertion


class ResultData(object):
    ''' Result data package object.
    '''
    def __init__(self, data: (list, Container, CodeList, RawData), is_succeeded: bool, error: BuilderError=None):
        self._data = assertion.is_various_types(data, (list, Container, CodeList, RawData))
        self._is_succeeded = assertion.is_bool(is_succeeded)
        self._error = error

    #
    # property
    #

    @property
    def data(self) -> (list, Container, CodeList, RawData):
        return self._data

    @property
    def is_succeeded(self) -> bool:
        return self._is_succeeded

    @property
    def error(self) -> (BuilderError, None):
        return self._error

