# -*- coding: utf-8 -*-
"""Define who class.
"""
from . import assertion
from .basesubject import BaseSubject
from .basedata import BaseData


class Who(BaseSubject):
    """For a pronoun class.
    """
    DEF_NAME = "__who__"

    def __init__(self):
        super().__init__(Who.DEF_NAME)


class Where(BaseData):
    """For a pronoun class as a stage.
    """
    DEF_NAME = "__where__"

    def __init__(self):
        super().__init__(Where.DEF_NAME)


class When(BaseData):
    """For a pronoun class as time and day.
    """
    DEF_NAME = "__when__"

    def __init__(self):
        super().__init__(When.DEF_NAME)
