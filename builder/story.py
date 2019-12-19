# -*- coding: utf-8 -*-
"""Define story container class.
"""
from . import assertion
from .basecontainer import BaseContainer
from .chapter import Chapter
from . import __DEF_PRIORITY__


class Story(BaseContainer):
    """The container for chapters.
    """
    def __init__(self, title: str, *args):
        super().__init__(title, __DEF_PRIORITY__)
        self._chapters = Story._validatedChapters(*args)

    def inherited(self, *chaps, title: str=None):
        return Story(self.title if not title else assertion.is_str(title),
                *chaps).setPriority(self.priority)

    @property
    def chapters(self): return self._chapters

    # private
    def _validatedChapters(*args):
        return args if [assertion.is_instance(v, Chapter) for v in args] else ()

