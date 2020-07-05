# -*- coding: utf-8 -*-
'''
Text List Object
================
'''

from __future__ import annotations

__all__ = ('TextList',)


from typing import Tuple
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class TextList(object):
    ''' Text list package object.
    '''
    def __init__(self, *args: str):
        self._data = tuple(assertion.is_instance(a, str) for a in args)

    #
    # property
    #

    @property
    def data(self) -> Tuple[str]:
        return self._data

