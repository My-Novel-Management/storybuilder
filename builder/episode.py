# -*- coding: utf-8 -*-
"""Define episode class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .scene import Scene
from .action import Action


class Episode(BaseContainer):
    """The container for scenes.
    """
    def __init__(self, title: str, outline: str, *args):
        super().__init__(title, Action.DEF_PRIORITY)
        self._outline = assertion.is_str(outline)
        self._scenes = Episode._validatedScenes(*args)

    def inherited(self, *scs):
        return Episode(self.title, self.outline, *scs).setPriority(self.priority)

    @property
    def outline(self): return self._outline

    @property
    def scenes(self): return self._scenes

    # private
    def _validatedScenes(*args):
        return args if [assertion.is_instance(v, Scene) for v in args] else ()
