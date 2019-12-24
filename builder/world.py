# -*- coding: utf-8 -*-
"""Define class that world management.
"""
from typing import Any
from . import assertion
from . import __DEF_LAYER__
from .action import Action, ActType, TagAction, TagType, Layer
from .basedata import BaseData
from .chapter import Chapter
from .combaction import CombAction
from .day import Day
from .description import Rubi, RubiType
from .episode import Episode
from .flag import Flag
from .item import Item
from .person import Person
from .scene import Scene
from .skin import PersonSkin
from .story import Story
from .stage import Stage
from .time import Time
from .word import Word


## defines
Subjects = (str, Person, None)


class UtilityDict(dict):
    """Useful dictionary class.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class World(UtilityDict):
    """World class.
    """
    # TODO:
    #   methods name convert camelCase
    MECAB_NEWDICT1 = "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd"
    MECAB_NEWDICT2 = "-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"

    def __init__(self, mecabdict: [int, str]=0):
        super().__init__()
        self.day = UtilityDict()
        self.item = UtilityDict()
        self.stage = UtilityDict()
        self.time = UtilityDict()
        self.word = UtilityDict()
        self._mecabdict = mecabdict if isinstance(mecabdict, str) else("" if mecabdict <= 0 else (World.MECAB_NEWDICT1 if mecabdict ==1 else World.MECAB_NEWDICT2))
        self._isConstractWords = False
        self._words = {}
        self._rubis = {}
        self._layers = {}

    @property
    def mecabdict(self): return self._mecabdict

    @property
    def words(self):
        from .buildtool import Build
        if self._isConstractWords:
            return self._words
        else:
            self._isConstractWords = True
            self._words = Build.constractWords(self)
            return self._words

    @property
    def rubis(self): return self._rubis

    @property
    def layers(self): return self._layers

    # creations
    def chapter(self, *args, **kwargs):
        '''To create a chapter.
        '''
        return Chapter(*args, **kwargs)

    def episode(self, *args, **kwargs):
        '''To create a episode.
        '''
        return Episode(*args, **kwargs)

    def scene(self, *args, **kwargs):
        '''To create a scene.
        '''
        return Scene(*args, **kwargs)

    def story(self, *args, **kwargs):
        '''To create a story.
        '''
        return Story(*args, **kwargs)

    # db management
    def append_day(self, key: str, val: Any):
        return self._appendOne(key, val, self.day, Day)

    def append_item(self, key: str, val: Any):
        return self._appendOne(key, val, self.item, Item)

    def append_person(self, key: str, val: Any):
        return self._appendOne(key, val, self, Person)

    def append_stage(self, key: str, val: Any):
        return self._appendOne(key, val, self.stage, Stage)

    def append_time(self, key: str, val: Any):
        return self._appendOne(key, val, self.time, Time)

    def append_word(self, key: str, val: Any):
        return self._appendOne(key, val, self.word, Word)

    def appendRubi(self, key: str, val: Any):
        def _rubtype(v):
            if v == 0: return RubiType.NOSET
            elif v == 2: return RubiType.EVERY
            else: return RubiType.ONCE
        self._rubis[key] = Rubi(val[0], val[1], val[2],
                _rubtype(val[3] if len(val) >= 4 else None))
        return self

    def appendLayer(self, key: str, val: Any):
        self._layers[key] = Layer(*val)
        return self

    def set_days(self, days: list):
        return self._setItemsFrom(days, self.append_day)

    def set_items(self, items: list):
        return self._setItemsFrom(items, self.append_item)

    def set_persons(self, persons: list):
        return self._setItemsFrom(persons, self.append_person)

    def set_stages(self, stages: list):
        return self._setItemsFrom(stages, self.append_stage)

    def set_times(self, times: list):
        return self._setItemsFrom(times, self.append_time)

    def set_words(self, words: list):
        return self._setItemsFrom(words, self.append_word)

    def setRubis(self, rubis: list):
        for v in assertion.is_list(rubis):
            self.appendRubi(v[0], v)
        return self

    def setLayers(self, layers: list):
        for v in assertion.is_list(layers):
            self.appendLayer(v[0], v[1:])
        return self

    def set_db(self, persons: list,
            stages: list, days: list, times: list,
            items: list, words: list): # pragma: no cover
        if persons:
            self.set_persons(persons)
        if items:
            self.set_items(items)
        if stages:
            self.set_stages(stages)
        if days:
            self.set_days(days)
        if times:
            self.set_times(times)
        if words:
            self.set_words(words)
        return self

    # controls
    # TODO: elapsed day and time control

    # actions
    def combine(self, *args):
        return CombAction(*args)

    def act(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.ACT, layer=layer)

    def be(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.BE, layer=layer)

    def come(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.COME, layer=layer)

    def go(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.GO, layer=layer)

    def have(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.HAVE, layer=layer)

    def hear(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.HEAR, layer=layer)

    def look(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.LOOK, layer=layer)

    def move(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.MOVE, layer=layer)

    def talk(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.TALK, layer=layer)

    def think(self, subject: Subjects,
            outline: str="", layer: str=__DEF_LAYER__):
        return Action(subject, outline, act_type=ActType.THINK, layer=layer)

    # tags
    def comment(self, info: str):
        return TagAction(info, tag_type=TagType.COMMENT)

    def br(self):
        return TagAction("", tag_type=TagType.BR)

    def hr(self):
        return TagAction("", tag_type=TagType.HR)

    def symbol(self, info: str):
        return TagAction(info, tag_type=TagType.SYMBOL)

    def title(self, info: str, subinfo: str="1"):
        return TagAction(info, subinfo, TagType.TITLE)

    def layer(self, info: str=__DEF_LAYER__):
        return TagAction(info, tag_type=TagType.SET_LAYER)

    # build
    def build(self, val: Story): # pragma: no cover
        '''To build this story world.
        '''
        from .buildtool import Build
        bd = Build(val, self.words, self.rubis, self.layers, self.mecabdict)
        return 0 if bd.outputStory() else 1

    # private
    def _appendOne(self, key: str, val: Any, body: [UtilityDict, dict],
            datatype: BaseData):
        if body is self:
            self.__setitem__(assertion.is_str(key), self._dataFrom(val, datatype))
        else:
            tmp = self._dataFrom(val, datatype)
            assertion.is_instance(body, UtilityDict).__setitem__(
                    assertion.is_str(key), tmp)
            # TODO:
            #   stage is On prefix only
            #   day is In prefix only
            #   time is At prefix only
            if isinstance(tmp, Stage):
                self.__setitem__('on_' + key, tmp)
            elif isinstance(tmp, Day):
                self.__setitem__('in_' + key, tmp)
            elif isinstance(tmp, Time):
                self.__setitem__('at_' + key, tmp)
        return self

    def _dataFrom(self, val: Any, datatype: BaseData):
        return val if isinstance(val, datatype) else datatype(*val)

    def _setItemsFrom(self, data: list, f):
        for v in assertion.is_list(data):
            f(v[0], v[1:])
        return self
