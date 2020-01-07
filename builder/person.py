# -*- coding: utf-8 -*-
"""Define data type of person
"""
## public libs
from __future__ import annotations
from typing import Tuple
## local libs
from utils import assertion
from utils.util_str import dictFromStrBySplitter, strDividedBySplitter
## local files
from builder.basedata import BaseData


## define class
class Person(BaseData):
    """The data class of person.

    Attributes:
        name (str): a person name.
        fullname (str): a full name base string.
        age (int): 0. an age.
        sex (str): 1. a sex.
        job (str): 2. a job.
        calling (dict): a calling dictionary.
        note (str): a note.
    """
    __CALLING__ = "me:私"
    __NOTE__ = "nothing"
    def __init__(self, name: str, fullname: str, age: int, sex: str, job: str,
            calling: [dict, str]=__CALLING__, note: str=__NOTE__):
        super().__init__(name,
                (assertion.isStr(fullname),
                    assertion.isInt(age),
                    assertion.isStr(sex),
                    assertion.isStr(job),
                    assertion.isDict(self._callingConstructed(calling, name)),
                    ),
                note=note,
                )

    ## property
    @property
    def fullname(self) -> str:
        return self.data[0]

    @property
    def age(self) -> int:
        return self.data[1]

    @property
    def sex(self) -> str:
        return self.data[2]

    @property
    def job(self) -> str:
        return self.data[3]

    @property
    def calling(self) -> dict:
        return self.data[4]

    ## method (class)
    @classmethod
    def fullnamesConstructed(cls, src: Person) -> tuple:
        tmp = src.fullname if assertion.isInstance(src, Person).fullname else src.name
        last, first = strDividedBySplitter(tmp, ",")
        full = tmp.replace(',', '')
        exfull = src.name
        if src.fullname:
            exfull = f"{first}・{last}"
        return (last, first, full, exfull)

    @classmethod
    def getGod(cls) -> Person:
        return Person("■", "", 99, "none", "god")

    ## privates
    def _callingConstructed(self, calling: (str, dict), name: str):
        tmp = dictFromStrBySplitter(calling, ":")
        me = tmp['me'] if 'me' in tmp else '私'
        return dict(tmp, **{'S':name, 'M':me})
