# -*- coding: utf-8 -*-
'''
Story Container Object
======================
'''

from __future__ import annotations

__all__ = ('Container',)


from builder.objects.sobject import SObject
from builder.utils import assertion


class Container(SObject):
    ''' Container base class.
    '''

    def __init__(self, title: str, *args: Any, outline: str=''):
        super().__init__(title)
        self._children = assertion.is_tuple(args)
        self._outline = assertion.is_str(outline)

    #
    # property
    #

    @property
    def children(self) -> list:
        return self._children

    @property
    def title(self) -> str:
        return self.name

    @property
    def outline(self) -> str:
        return self._outline

    #
    # methods
    #

    def inherited(self, *args: Any,
            title: str=None, outline: str=None) -> Container:
        return self.__class__(
                title if title else self.title,
                *args,
                outline=outline if outline else self.outline,
                ).set_priority(self.priority)

