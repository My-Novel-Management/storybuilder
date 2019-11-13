# -*- coding: utf-8 -*-
"""Define person subject class.
"""
from . import assertion
from .basesubject import BaseSubject
from .strutils import divided_by_splitter, str_to_dict_by_splitter


class Person(BaseSubject):
    """Data type of person subject.
    """
    DEF_CALLING = "me:私"
    DEF_NOTE = "なし"
    DEF_FEATURES = "hair:黒髪"

    def __init__(self, name: str, fullname: str, age: int, sex: str, job: str,
            calling: [dict, str]=DEF_CALLING, note: str=DEF_NOTE,
            features: [dict, str]=DEF_FEATURES):
        super().__init__(name)
        # TODO: 名前をフルとか分割して登録
        _fullname = fullname if fullname and isinstance(fullname, str) else name
        self._lastname, self._firstname = divided_by_splitter(_fullname)
        self._fullname = _fullname.replace(',', '')
        self._exfullname = _fullname.replace(',', '・')
        self._age = assertion.is_int(age)
        self._sex = assertion.is_str(sex)
        self._job = assertion.is_str(job)
        self._note = assertion.is_str(note)
        self._calling = Person._appendedBaseCalling(str_to_dict_by_splitter(calling), name)
        self._features = str_to_dict_by_splitter(features)

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

    @property
    def features(self): return self._features

    # privets
    def _appendedBaseCalling(origin: dict, name: str):
        me = origin['me'] if 'me' in origin else '私'
        return dict(origin, **{'S':name, 'M':me})

