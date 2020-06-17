# -*- coding: utf-8 -*-
'''
Raw Data Object
===============
'''

from __future__ import annotations

__all__ = ('RawData',)


from typing import Tuple
from builder.commands.scode import SCode
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.formattag import FormatTag
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class RawData(object):
    ''' Raw Data package object.
    '''
    def __init__(self, *args: (str, FormatTag)):
        self._data = tuple(assertion.is_instance(a, (str, FormatTag)) for a in args)

    #
    # property
    #

    @property
    def data(self) -> Tuple[(str, FormatTag)]:
        return self._data

