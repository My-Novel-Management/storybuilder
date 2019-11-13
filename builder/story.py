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
        super().__init__(title, Action.DEF_PRIORITY)
        self._chapters = Story._validatedChapters(*args)

    def inherited(self, *chaps):
        return Story(self.title, *chaps).setPriority(self.priority)

    @property
    def chapters(self): return self._chapters

    # private
    def _validatedChapters(*args):
        for a in args:
            if not isinstance(a, Chapter):
                raise AssertionError("Must be data type of 'Chapter'")
        return args

