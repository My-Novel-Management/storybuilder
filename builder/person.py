# -*- coding: utf-8 -*-
"""Define person subject class.
"""
from __future__ import annotations
from . import assertion
from .basesubject import BaseSubject
from .strutils import divided_by_splitter, str_to_dict_by_splitter


class Person(BaseSubject):
    """Data type of person subject.
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
        super().__init__(name)
        _fullname = fullname if fullname and isinstance(fullname, str) else name
        self._lastname, self._firstname = divided_by_splitter(_fullname)
        self._fullname = _fullname.replace(',', '')
        self._exfullname = _fullname.replace(',', '・')
        self._age = assertion.is_int(age)
        self._sex = assertion.is_str(sex)
        self._job = assertion.is_str(job)
        self._note = assertion.is_str(note)
        self._calling = Person._appendedBaseCalling(str_to_dict_by_splitter(calling), name)
        # TODO: 髪色や髪型などはskinみたいなデータ型を作るか、itemを流用して
        #       後付できるようにする
        #       stageなどの設定と同じ

    @staticmethod
    def Boy(name: str, age: int=__AGE_CHILD__, job: str=__JOB_CHILD__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__MALE__, job, calling, "")

    def Girl(name: str, age: int=__AGE_CHILD__, job: str=__JOB_CHILD__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__FEMALE__, job, calling, "")

    def TeenBoy(name: str, age: int=__AGE_TEEN__, job: str=__JOB_TEEN__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__MALE__, job, calling, "")

    def TeenGirl(name: str, age: int=__AGE_TEEN__, job: str=__JOB_TEEN__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__FEMALE__, job, calling, "")

    def Man(name: str, age: int=__AGE__, job: str=__JOB__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__MALE__, job, calling, "")

    def Woman(name: str, age: int=__AGE__, job: str=__JOB__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__FEMALE__, job, calling, "")

    def OldMan(name: str, age: int=__AGE_OLD__, job: str=__JOB_OLD__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__MALE__, job, calling, "")

    def OldWoman(name: str, age: int=__AGE_OLD__, job: str=__JOB_OLD__,
            calling: (str, dict)=__CALLING__) -> __class__:
        return Person(name, "", age, Person.__FEMALE__, job, calling, "")

    @property
    def firstname(self): return self._firstname

    @property
    def lastname(self): return self._lastname

    @property
    def fullname(self): return self._fullname

    @property
    def exfullname(self): return self._exfullname

    @property
    def age(self): return self._age

    @property
    def sex(self): return self._sex

    @property
    def job(self): return self._job

    @property
    def note(self): return self._note

    @property
    def calling(self): return self._calling

    def inherited(self, name: str, fullname: str=None, age: int=None, sex: str=None,
            job: str=None, calling: [dict, str]=None, note: str=None):
        return Person(name,
                fullname if fullname else (f"{self.lastname},{self.firstname}" if self.lastname != self.firstname else ""),
                assertion.is_int(age) if age else self.age,
                assertion.is_str(sex) if sex else self.sex,
                assertion.is_str(job) if job else self.job,
                assertion.is_instance(calling, (str, dict)) if calling else self.calling,
                assertion.is_str(note) if note else self.note
                )
    # privets
    def _appendedBaseCalling(origin: dict, name: str):
        me = origin['me'] if 'me' in origin else '私'
        return dict(origin, **{'S':name, 'M':me})

