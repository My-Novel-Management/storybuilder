# -*- coding: utf-8 -*-
"""Define who class.
"""
from . import assertion
from .basesubject import BaseSubject
from .basedata import BaseData


class Who(BaseSubject):
    """For a pronoun class.
    """
    __NAME__ = "__who__"

    def __init__(self):
        super().__init__(Who.__NAME__)

    ## override operator
    def __eq__(self, obj):
        return isinstance(obj, Who) and self.name == obj.name


class Where(BaseData):
    """For a pronoun class as a stage.
    """
    __NAME__ = "__where__"

    def __init__(self):
        super().__init__(Where.__NAME__)


class When(BaseData):
    """For a pronoun class as time and day.
    """
    __NAME__ = "__when__"

    def __init__(self):
        super().__init__(When.__NAME__)
