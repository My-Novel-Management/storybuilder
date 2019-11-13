# -*- coding: utf-8 -*-
"""Define chapter class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .episode import Episode
from .action import Action


class Chapter(BaseContainer):
    """The container for episodes.
    """
    def __init__(self, title: str, *args):
        super().__init__(title, Action.DEF_PRIORITY)
        self._episodes = Chapter._validatedEpisodes(*args)

    def inherited(self, *epis):
        return Chapter(self.title, *epis).setPriority(self.priority)

    @property
    def episodes(self): return self._episodes

    # privates
    def _validatedEpisodes(*args):
        for a in args:
            if not isinstance(a, Episode):
                raise AssertionError("Must be data type of 'Episode'!")
        return args

