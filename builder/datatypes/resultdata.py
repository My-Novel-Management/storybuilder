# -*- coding: utf-8 -*-
'''
Result Data Object
==================
'''

from __future__ import annotations

__all__ = ('ResultData',)


from analyzer.datatypes.tokenlist import TokenList
from builder.containers.container import Container
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.rawdata import RawData
from builder.datatypes.textlist import TextList
from builder.utils import assertion


class ResultData(object):
    ''' Result data package object.
    '''
    def __init__(self, data: (list, Container, CodeList, RawData, TextList, TokenList), is_succeeded: bool, error: BuilderError=None):
        self._data = assertion.is_various_types(data, (list, Container, CodeList, RawData, TextList, TokenList))
        self._is_succeeded = assertion.is_bool(is_succeeded)
        self._error = error

    #
    # property
    #

    @property
    def data(self) -> (list, Container, CodeList, RawData, TextList, TokenList):
        return self._data

    @property
    def is_succeeded(self) -> bool:
        return self._is_succeeded

    @property
    def error(self) -> (BuilderError, None):
        return self._error

