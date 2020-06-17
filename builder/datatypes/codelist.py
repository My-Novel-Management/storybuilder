# -*- coding: utf-8 -*-
'''
Code List Object
===============
'''

from __future__ import annotations

__all__ = ('CodeList',)


from typing import Tuple
from builder.commands.scode import SCode
from builder.datatypes.builderexception import BuilderError
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class CodeList(object):
    ''' Code list package object.
    '''
    def __init__(self, *args: SCode):
        self._data = tuple(assertion.is_instance(a, SCode) for a in args)

    #
    # property
    #

    @property
    def data(self) -> Tuple[SCode]:
        return self._data

