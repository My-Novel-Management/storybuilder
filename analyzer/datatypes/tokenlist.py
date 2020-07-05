# -*- coding: utf-8 -*-
'''
Token List Object
=================
'''

from __future__ import annotations

__all__ = ('TokenList',)


from typing import Tuple
from analyzer.datatypes.mecabdata import MecabData
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class TokenList(object):
    ''' Token list package object.
    '''
    def __init__(self, *args: MecabData):
        self._data = tuple(assertion.is_instance(a, MecabData) for a in args)

    #
    # property
    #

    @property
    def data(self) -> Tuple[MecabData]:
        return self._data

