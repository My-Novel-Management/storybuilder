# -*- coding: utf-8 -*-
'''
Plot Information Data
=====================
'''

from __future__ import annotations

__all__ = ('PlotInfo',)


from builder.utils import assertion


class PlotInfo(object):
    ''' Plot Info Data class.
    '''
    def __init__(self, title: str, *args):
        self._title = assertion.is_str(title)
        self._data = assertion.is_tuple(args)

    #
    # property
    #

    @property
    def title(self) -> str:
        return self._title

    @property
    def data(self) -> tuple:
        return self._data

