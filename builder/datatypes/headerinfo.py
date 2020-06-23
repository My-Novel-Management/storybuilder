# -*- coding: utf-8 -*-
'''
Header Information Data
=======================
'''

from __future__ import annotations

__all__ = ('HeaderInfo',)


from builder.utils import assertion


class HeaderInfo(object):
    ''' Header Info Data class.
    '''
    def __init__(self, total_chars: int, desc_chars: int,
            lines: int, papers: (int, float),
            chapters: int, episodes: int, scenes: int, scodes: int):
        self._total_chars = assertion.is_int(total_chars)
        self._desc_chars = assertion.is_int(desc_chars)
        self._lines = assertion.is_int(lines)
        self._papers = assertion.is_int_or_float(papers)
        self._chapters = assertion.is_int(chapters)
        self._episodes = assertion.is_int(episodes)
        self._scenes = assertion.is_int(scenes)
        self._scodes = assertion.is_int(scodes)

    #
    # property
    #

    @property
    def total_chars(self) -> int:
        return self._total_chars

    @property
    def desc_chars(self) -> int:
        return self._desc_chars

    @property
    def lines(self) -> int:
        return self._lines

    @property
    def papers(self) -> (int, float):
        return self._papers

    @property
    def chapters(self) -> int:
        return self._chapters

    @property
    def episodes(self) -> int:
        return self._episodes

    @property
    def scenes(self) -> int:
        return self._scenes

    @property
    def scodes(self) -> int:
        return self._scodes

    #
    # methods
    #

