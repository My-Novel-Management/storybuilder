# -*- coding: utf-8 -*-
"""Define data type of person
"""
## public libs
from __future__ import annotations
from typing import Tuple
## local libs
from utils import assertion
from utils import util_str as sutil
## local files
from builder.basedata import BaseData


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
    __MALE__ = "male"
    __FEMALE__ = "female"
    __AGE_CHILD__ = 10
    __AGE_TEEN__ = 15
    __AGE__ = 25
    __AGE_OLD__ = 60
    __JOB_CHILD__ = "小学生"
    __JOB_TEEN__ = "学生"
    __JOB__ = "会社員"
    __JOB_OLD__ = "無職"
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
                    assertion.isStr(note),
                    )
                )

    ## static methods
    @classmethod
    def getGod(cls) -> Person:
        return Person("__", "", 999, "none", "god")

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

    @property
    def note(self) -> str:
        return self.data[5]

    ## privates
    def _callingConstructed(self, calling: (str, dict), name: str):
        tmp = sutil.dictFromStrBySplitter(calling, ":")
        me = tmp['me'] if 'me' in tmp else '私'
        return dict(tmp, **{'S':name, 'M':me})
