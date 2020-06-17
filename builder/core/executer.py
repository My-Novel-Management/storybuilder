# -*- coding: utf-8 -*-
'''
Executer Object
===============
'''

from __future__ import annotations

__all__ = ('Executer',)


from abc import ABC, abstractmethod
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion


class Executer(ABC):
    ''' Executer class.
    '''

    #
    # methods
    #

    @abstractmethod
    def execute(self, *args, **kwargs) -> ResultData:
        pass
