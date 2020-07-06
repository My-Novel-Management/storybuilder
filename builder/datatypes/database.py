# -*- coding: utf-8 -*-
'''
Story Database Object
=====================
'''

from __future__ import annotations

__all__ = ('Database',)


from typing import Any, Callable
from builder.datatypes.builderexception import BuilderError
from builder.objects.day import Day
from builder.objects.item import Item
from builder.objects.person import Person
from builder.objects.rubi import Rubi
from builder.objects.sobject import SObject
from builder.objects.stage import Stage
from builder.objects.time import Time
from builder.objects.word import Word
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
ListLike = (list, tuple)

# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class DatabaseError(BuilderError):
    ''' DB General Error
    '''
    pass


class Database(object):
    ''' Database object class for a story data.
    '''

    __ASSET_ELEMENTS__ = ('PERSONS', 'STAGES', 'DAYS', 'TIMES', 'ITEMS', 'WORDS', 'RUBIS')

    def __init__(self):
        LOG.info('DB: initialize')
        self._persons = {}
        self._stages = {}
        self._days = {}
        self._times = {}
        self._items = {}
        self._words = {}
        self._rubis = {}
        self._tags = {}
        # default settings
        self.append_person('who', 'ある人', '', 30,(1,1), 'male', '会社員')

    #
    # property
    #

    @property
    def persons(self) -> dict:
        return self._persons

    @property
    def stages(self) -> dict:
        return self._stages

    @property
    def days(self) -> dict:
        return self._days

    @property
    def times(self) -> dict:
        return self._times

    @property
    def items(self) -> dict:
        return self._items

    @property
    def words(self) -> dict:
        return self._words

    @property
    def rubis(self) -> dict:
        return self._rubis

    @property
    def tags(self) -> dict:
        return self._tags

    #
    # methods
    #

    def get(self, key: str) -> SObject:
        if assertion.is_str(key) in self.persons:
            return self._persons[key]
        elif key in self.stages:
            return self._stages[key]
        elif key.startswith('on_') and key.replace('on_','') in self.stages:
            return self._stages[key.replace('on_', '')]
        elif key in self.days:
            return self._days[key]
        elif key.startswith('in_') and key.replace('in_','') in self.days:
            return self._days[key.replace('in_','')]
        elif key in self.times:
            return self._times[key]
        elif key.startswith('at_') and key.replace('at_','') in self.times:
            return self._times[key.replace('at_','')]
        elif key in self.items:
            return self._items[key]
        elif key.startswith('i_') and key.replace('i_','') in self.items:
            return self._items[key.replace('i_','')]
        elif key in self.words:
            return self._words[key]
        elif key.startswith('w_') and key.replace('w_','') in self.words:
            return self._words[key.replace('w_','')]
        else:
            msg = f'Not found the key in DB: {key}'
            LOG.error(msg)
            return None

    def get_person_names(self) -> list:
        tmp = []
        for val in self._persons.values():
            tmp.append(val.name)
            tmp.append(val.firstname)
            tmp.append(val.lastname)
            tmp.append(val.fullname)
            tmp.append(val.exfullname)
        return list(set(tmp))

    def build_db(self, persons: ListLike, stages: ListLike, days: ListLike,
            times: ListLike, items: ListLike, words: ListLike,
            rubis: ListLike) -> None:
        # TODO: 間違ったものの設定時はエラー出す
        if assertion.is_listlike(persons):
            self.set_persons(persons)
        if assertion.is_listlike(stages):
            self.set_stages(stages)
        if assertion.is_listlike(days):
            self.set_days(days)
        if assertion.is_listlike(times):
            self.set_times(times)
        if assertion.is_listlike(items):
            self.set_items(items)
        if assertion.is_listlike(words):
            self.set_words(words)
        if assertion.is_listlike(rubis):
            self.set_rubis(rubis)

    def set_from_asset(self, asset: dict) -> None:
        for elm in self.__ASSET_ELEMENTS__:
            if elm.upper() in assertion.is_dict(asset):
                if elm.lower() == 'persons':
                    self.set_persons(asset[elm.upper()])
                elif elm.lower() == 'stages':
                    self.set_stages(asset[elm.upper()])
                elif elm.lower() == 'days':
                    self.set_days(asset[elm.upper()])
                elif elm.lower() == 'times':
                    self.set_times(asset[elm.upper()])
                elif elm.lower() == 'items':
                    self.set_items(asset[elm.upper()])
                elif elm.lower() == 'words':
                    self.set_words(asset[elm.upper()])
                elif elm.lower() == 'rubis':
                    self.set_rubis(asset[elm.upper()])
                else:
                    msg = f'Asset name mismatch!: {elm.upper()}'
                    LOG.error(msg)

    def set_persons(self, persons: ListLike) -> None:
        self._set_objects(persons, self.append_person)

    def set_stages(self, stages: ListLike) -> None:
        self._set_objects(stages, self.append_stage)

    def set_days(self, days: ListLike) -> None:
        self._set_objects(days, self.append_day)

    def set_times(self, times: ListLike) -> None:
        self._set_objects(times, self.append_time)

    def set_items(self, items: ListLike) -> None:
        self._set_objects(items, self.append_item)

    def set_words(self, words: ListLike) -> None:
        self._set_objects(words, self.append_word)

    def set_rubis(self, rubis: ListLike) -> None:
        self._set_objects(rubis, self.append_rubi)

    def append_person(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Person)

    def append_stage(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Stage)

    def append_day(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Day)

    def append_time(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Time)

    def append_item(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Item)

    def append_word(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Word)

    def append_rubi(self, key: str, *args: Any) -> None:
        self._append_object(key, *args, obj=Rubi)

    #
    # private methods
    #

    def _append_object(self, key: str, *args: Any, obj: SObject) -> None:
        if obj is Person:
            tmp = Person(*args)
            self._persons[assertion.is_str(key)] = tmp
            self._tags[key] = tmp.name
            self._tags['n_' + key] = tmp.name
            self._tags['ln_' + key] = tmp.lastname
            self._tags['fn_' + key] = tmp.firstname
            self._tags['full_' + key] = tmp.fullname
            self._tags['exfull_' + key] = tmp.exfullname
        elif obj is Stage:
            tmp = Stage(*args)
            self._stages[assertion.is_str(key)] = tmp
            self._tags[key] = tmp.name
            self._tags['on_' + key] = tmp.name
        elif obj is Day:
            tmp = Day(*args)
            self._days[assertion.is_str(key)] = tmp
            self._tags[key] = tmp.name
            self._tags['in_' + key] = tmp.name
        elif obj is Time:
            tmp = Time(*args)
            self._times[assertion.is_str(key)] = tmp
            self._tags[key] = tmp.name
            self._tags['at_' + key] = tmp.name
        elif obj is Item:
            tmp = Item(*args)
            self._items[assertion.is_str(key)] = tmp
            self._tags[key] = tmp.name
            self._tags['i_' + key] = tmp.name
        elif obj is Word:
            tmp = Word(*args)
            self._words[assertion.is_str(key)] = tmp
            self._tags[key] = tmp.name
            self._tags['w_' + key] = tmp.name
        elif obj is Rubi:
            self._rubis[assertion.is_str(key)] = Rubi(key, *args)
        else:
            msg = f'Unknown a story object for appending to DB: {obj}'
            LOG.error(msg)

    def _set_objects(self, data: ListLike, func: Callable) -> None:
        for line in assertion.is_listlike(data):
            func(line[0], *line[1:])
