# -*- coding: utf-8 -*-
"""Define pronoun data types.
"""
## public libs
import datetime
## local libs
from utils import assertion
## local files
from builder import __DEF_YEAR__, __DEF_MON__, __DEF_DAY__
from builder.basedata import BaseData


class Who(BaseData):
    """The pronoun data for Person
    """
    __NAME__ = "__who__"
    def __init__(self):
        super().__init__(Who.__NAME__, None)


class When(BaseData):
    """The pronoun data for Day, Time
    """
    __NAME__ = "__when__"
    def __init__(self):
        super().__init__(When.__NAME__,
                datetime.date(year=__DEF_YEAR__, month=__DEF_MON__, day=__DEF_DAY__))


class Where(BaseData):
    """The pronoun data for Stage
    """
    __NAME__ = "__where__"
    def __init__(self):
        super().__init__(Where.__NAME__, None)


class That(BaseData):
    """The pronoun data for Item, Word
    """
    __NAME__ = "__that__"
    def __init__(self):
        super().__init__(That.__NAME__, None)
