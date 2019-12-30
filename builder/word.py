# -*- coding: utf-8 -*-
"""Define data type of word
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.basedata import BaseData


class Word(BaseData):
    """The data class of word.

    Attributes:
        name (str): a word name
        note (str): 0. a note
    """
    def __init__(self, name: str, note: str=""):
        super().__init__(name,
                (assertion.isStr(note),
                    ))

    ## property
    @property
    def note(self) -> str:
        return self.data[0]
