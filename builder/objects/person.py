# -*- coding: utf-8 -*-
'''
Person Object
=============
'''

from __future__ import annotations

__all__ = ('Person',)


from builder.objects.sobject import SObject
from builder.utils import assertion
from builder.utils.util_dict import calling_dict_from
from builder.utils.util_name import name_set_from


class Person(SObject):
    ''' Person Object class.
    '''

    def __init__(self, name: str, fullname: str,
            age: int, birth: tuple, sex: str, job: str,
            calling: (str, dict)='me:私', info: str=''):
        super().__init__(name)
        self._basename = assertion.is_str(fullname)
        self._age = assertion.is_int(age)
        self._birth = assertion.is_tuple(birth)
        self._sex = assertion.is_str(sex)
        self._job = assertion.is_str(job)
        self._calling = calling_dict_from(calling, name)
        self._info = assertion.is_str(info)
        # names
        self._firstname, self._lastname, self._fullname, self._exfullname = name_set_from(self._basename, name)

    #
    # property
    #

    @property
    def age(self) -> int:
        return self._age

    @property
    def birth(self) -> tuple:
        return self._birth

    @property
    def sex(self) -> str:
        return self._sex

    @property
    def job(self) -> str:
        return self._job

    @property
    def calling(self) -> dict:
        return self._calling

    @property
    def info(self) -> str:
        return self._info

    @property
    def firstname(self) -> str:
        return self._firstname

    @property
    def lastname(self) -> str:
        return self._lastname

    @property
    def fullname(self) -> str:
        return self._fullname

    @property
    def exfullname(self) -> str:
        return self._exfullname

