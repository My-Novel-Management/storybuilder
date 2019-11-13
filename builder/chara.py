# -*- coding: utf-8 -*-
"""Define other subject class.
"""
from . import assertion
from .basesubject import BaseSubject


class Chara(BaseSubject):
    """Data type of other subject.
    """
    def __init__(self, name: str):
        super().__init__(name)

