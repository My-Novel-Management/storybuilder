# -*- coding: utf-8 -*-
"""Define story container class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .chapter import Chapter


class Story(BaseContainer):
    """The container for chapters.
    """
    def __init__(self, title: str, *args):
        from .action import Action
        # TODO: あとで__DEF_PRIORITY__を利用する
        super().__init__(title, Action.DEF_PRIORITY)
        self._chapters = Story._validatedChapters(*args)

    def inherited(self, *chaps):
        return Story(self.title, *chaps).setPriority(self.priority)

    @property
    def chapters(self): return self._chapters

    # private
    def _validatedChapters(*args):
        return args if [assertion.is_instance(v, Chapter) for v in args] else ()

