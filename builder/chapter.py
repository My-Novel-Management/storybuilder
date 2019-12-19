# -*- coding: utf-8 -*-
"""Define chapter class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .episode import Episode
from . import __DEF_PRIORITY__


class Chapter(BaseContainer):
    """The container for episodes.
    """
    def __init__(self, title: str, *args):
        super().__init__(title, __DEF_PRIORITY__)
        self._episodes = Chapter._validatedEpisodes(*args)

    def inherited(self, *epis, title: str=None):
        return Chapter(self.title if not title else assertion.is_str(title),
                *epis).setPriority(self.priority)

    @property
    def episodes(self): return self._episodes

    # privates
    def _validatedEpisodes(*args):
        return args if [assertion.is_instance(v, Episode) for v in args] else ()

