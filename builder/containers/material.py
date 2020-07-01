# -*- coding: utf-8 -*-
'''
Material Container Object
========================
'''

from __future__ import annotations

__all__ = ('Material',)


from typing import Any
from builder.containers.container import Container
from builder.datatypes.materialtype import MaterialType
from builder.utils import assertion


class Material(Container):
    ''' Material Container class.
    '''

    def __init__(self,
            mate_type: MaterialType,
            title: str,
            *args: Any,
            outline: str=''):
        super().__init__(title, *args, outline=outline)
        self._mate_type = assertion.is_instance(mate_type, MaterialType)
    #
    # property
    #

    @property
    def mate_type(self) -> MaterialType:
        return self._mate_type

    #
    # methods
    #
    def inherited(self, *args: Any,
            title: str=None,
            outline: str=None) -> Material:
        return self.__class__(self.mate_type,
                title if title else self.title,
                *args,
                outline=outline if outline else self.outline,
                ).set_priority(self.priority)
