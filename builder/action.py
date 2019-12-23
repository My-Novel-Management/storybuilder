# -*- coding: utf-8 -*-
"""Define action class.
"""
from enum import Enum
from . import assertion
from .basedata import BaseData
from .description import Description, NoDesc, DescType
from .flag import Flag, NoFlag, NoDeflag
from .basesubject import NoSubject
from .person import Person
from .chara import Chara
from .who import Who
from . import __DEF_PRIORITY__, __MAX_PRIORYTY__, __MIN_PRIORITY__
from . import __DEF_LAYER__, __MAIN_LAYER__

class ActType(Enum):
    """Action type.
    """
    ACT = "act" # 全般
    BE = "be" # 外部状態
    COME = "come" # 出現
    GO = "go" # 消去
    HAVE = "have" # 所有変更
    HEAR = "hear" # 効果音などの音声
    LOOK = "look" # 描画
    MOVE = "move" # 動かす
    TALK = "talk" # 台詞
    TAG = "tag" # for tag
    THINK = "think" # 内部状態


class TagType(Enum):
    """Tag type
    """
    BR = "breakline" # BR
    COMMENT = "comment" # コメント
    HR = "horizontalline" # HR
    SYMBOL = "symbol" # シンボル
    TITLE = "title" # タイトル
    SET_LAYER = "layer" # レイヤー用


class Action(BaseData):
    """Data type of an action.
    """
    __NAME__ = "__action__"

    def __init__(self, subject: [Person, Chara, None],
            outline: str="", act_type: ActType=ActType.ACT,
            layer: str=__DEF_LAYER__):
        super().__init__(Action.__NAME__)
        _subject_is_str = isinstance(subject, str)
        self._subject = Action._validatedSubject(subject)
        self._outline = assertion.is_str(subject if _subject_is_str else outline)
        self._act_type = assertion.is_instance(act_type, ActType)
        self._description = NoDesc()
        self._flag = NoFlag()
        self._deflag = NoDeflag()
        self._priority = __DEF_PRIORITY__
        self._layer = assertion.is_str(layer)

    def inherited(self, subject=None, outline=None, desc=None):
        return Action(
                subject if subject else self.subject,
                outline if outline else self.outline,
                self.act_type) \
                    .flag(self.getFlag()).deflag(self.getDeflag()) \
                    ._setDescription(desc if desc else self.description,
                            self.description.desc_type) \
                    .setPriority(self.priority) \
                    .setLayer(self.layer)

    @property
    def act_type(self): return self._act_type

    @property
    def subject(self): return self._subject

    @property
    def outline(self): return self._outline

    @property
    def description(self): return self._description

    @property
    def priority(self): return self._priority

    @property
    def layer(self): return self._layer

    def setPriority(self, pri: int):
        self._priority = assertion.is_between(
                assertion.is_int(pri), __MAX_PRIORYTY__, __MIN_PRIORITY__)
        return self

    def setLayer(self, layer: str):
        self._layer = assertion.is_str(layer)
        return self

    def flag(self, val: [str, NoFlag]):
        # TODO: Flag がdeflagも兼ねているのでobjectのままset時に確認必要
        if isinstance(val, Flag):
            self._flag = val
        elif isinstance(val, str):
            self._flag = Flag(val)
        else:
            self._flag = NoFlag()
        return self

    def deflag(self, val: [str, NoDeflag]):
        if isinstance(val, Flag):
            self._deflag = val
        elif isinstance(val, str):
            self._deflag = Flag(val, True)
        else:
            self._deflag = NoDeflag()
        return self

    def getFlag(self): return self._flag

    def getDeflag(self): return self._deflag

    def omit(self):
        self._priority = __MIN_PRIORITY__
        return self

    # methods
    def desc(self, *args):
        self._description = Description(*args, desc_type=DescType.DESC)
        return self

    def d(self, *args): return self.desc(*args)

    def tell(self, *args):
        self._description = Description(*args, desc_type=DescType.DIALOGUE)
        return self

    def t(self, *args): return self.tell(*args)

    def comp(self, *args):
        self._description = Description(*args, desc_type=DescType.COMPLEX)
        return self

    def same(self, desc_type: str=None):
        if not desc_type:
            desc_type = 't' if self.act_type is ActType.TALK else 'd'
        if desc_type in ('t', 'tell'):
            self.tell(self.outline)
        elif desc_type in ('c', 'comp'):
            self.comp(self.outline)
        else:
            self.desc(self.outline)
        return self

    # private
    def _validatedSubject(sub: [str, Person, Chara, None]):
        if isinstance(sub, str):
            return Who()
        elif isinstance(sub, (Person, Chara, Who)):
            return sub
        else:
            return NoSubject()

    def _setDescription(self, descs, desc_type: DescType):
        if isinstance(descs, Description):
            self._description = descs
        elif isinstance(descs, str):
            self._description = Description(descs, desc_type=desc_type)
        else:
            self._description = Description(*descs,
                    desc_type=desc_type)
        return self


class TagAction(Action):

    def __init__(self, info: str, subinfo: str="", tag_type: TagType=TagType.COMMENT):
        super().__init__(None, info, ActType.TAG)
        self._subinfo = assertion.is_str(subinfo)
        self._tag_type = assertion.is_instance(tag_type, TagType)

    @property
    def info(self): return self._outline

    @property
    def subinfo(self): return self._subinfo

    @property
    def tag_type(self): return self._tag_type

    def inherited(self):
        return TagAction(self.info, self.subinfo, self.tag_type)

class Layer(BaseData):
    """Data type of a layer
    """
    def __init__(self, name: str, words: (str, list, tuple)):
        super().__init__(name)
        self._words = words

    @property
    def words(self): return self._words

