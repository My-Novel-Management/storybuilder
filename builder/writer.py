# -*- coding: utf-8 -*-
"""Define writer class.
"""
from enum import Enum
from typing import Optional
from . import assertion
from . import __DEF_LAYER__
from .action import Action, ActType
from .person import Person
from .who import Who
SomeOnes = (Person, Who)


class Does(Enum):
    ATTENTION = "気にする"
    AWAKE = "目覚める"
    BE = "いる"
    CLIMB = "登る"
    COME = "来る"
    CONFUSE = "戸惑う"
    CONSIDER = "考える"
    CRY = "叫ぶ"
    DISPLAY = "映る"
    DOWN = "降りる"
    DRINK = "飲む"
    EAT = "食べる"
    EXPRESSION = "表情をする"
    FALLDOWN = "倒れる"
    FEEL = "感じる"
    FLY = "飛ぶ"
    FUN = "楽しい"
    GAZE = "見つめる"
    GLAD = "嬉しい"
    GO = "行く"
    HEAR = "聞く"
    HURT = "傷つく"
    IMAGINE = "想像する"
    ISA = "である" # is a
    LAUGH = "笑う"
    LOOK = "見る"
    MAKE = "作る"
    MOVE = "移動する"
    NOD = "頷く"
    NOTICE = "気づく"
    OBTAIN = "手に入れる"
    PEEP = "覗く"
    PUTON = "履く"
    READ = "読む"
    REFUSE = "首を横に振る"
    REMEMBER = "思い出す"
    REPLY = "返事する"
    RUN = "走る"
    SAD = "悲しい"
    SIT = "座る"
    SLEEP = "眠る"
    TEARS = "泣く"
    TAKEOFF = "脱ぐ"
    THINK = "思う"
    WALK = "歩く"
    WEAR = "着る"
    WONDER = "不思議に思う"
    WRITE = "書く"


class Writer(object):
    """Utility tool for writing documents.
    """
    def __init__(self, subject: SomeOnes=Who(), is_displayS: bool=True):
        self._subject = assertion.is_instance(subject, SomeOnes)

    @property
    def subject(self): return self._subject

    ## basic action
    def do(self, doing: str, subject: Optional[Person]=None,
            obj: str="",
            act_type: ActType=ActType.ACT,
            layer: str=__DEF_LAYER__) -> Action:
        def _convS(subject):
            if subject:
                if not isinstance(subject, Who):
                    return f"{subject.name}は"
                else:
                    return ""
            else:
                if isinstance(self.subject, Person):
                    return f"{self.subject.name}は"
                else:
                    return ""
        sbj = _convS(subject)
        return Action(self._validatedSubject(subject), f"{sbj}{obj}{doing}",
                act_type=act_type, layer=layer)

    def talk(self, outline: str="", subject: Optional[Person]=None,
            layer: str=__DEF_LAYER__) -> Action:
        return Action(self._validatedSubject(subject), outline,
                act_type=ActType.TALK, layer=layer)

    ## actions
    def attention(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.ATTENTION, doing),
                subject, obj, ActType.THINK)

    def awake(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.AWAKE, doing),
                subject, obj, ActType.ACT)

    def be(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.BE, doing),
                subject, obj, ActType.BE)

    def climb(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.CLIMB, doing),
                subject, obj, ActType.MOVE)

    def come(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.COME, doing),
                subject, obj, ActType.COME)

    def confuse(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.CONFUSE, doing),
                subject, obj, ActType.THINK)

    def consider(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.CONSIDER, doing),
                subject, obj, ActType.THINK)

    def cry(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.CRY, doing),
                subject, obj, ActType.ACT)

    def display(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.DISPLAY, doing),
                subject, obj, ActType.LOOK)

    def down(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.DOWN, doing),
                subject, obj, ActType.MOVE)

    def drink(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.DRINK, doing),
                subject, obj, ActType.HAVE)

    def eat(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.EAT, doing),
                subject, obj, ActType.HAVE)

    def expression(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.EXPRESSION, doing),
                subject, obj, ActType.BE)

    def falldown(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.FALLDOWN, doing),
                subject, obj, ActType.MOVE)

    def feel(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.FEEL, doing),
                subject, obj, ActType.THINK)

    def fly(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.FLY, doing),
                subject, obj, ActType.ACT)

    def fun(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.FUN, doing),
                subject, obj, ActType.THINK)

    def gaze(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.GAZE, doing),
                subject, obj, ActType.LOOK)

    def glad(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.GLAD, doing),
                subject, obj, ActType.THINK)

    def go(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.GO, doing),
                subject, obj, ActType.GO)

    def hear(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.HEAR, doing),
                subject, obj, ActType.HEAR)

    def hurt(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.HURT, doing),
                subject, obj, ActType.THINK)

    def imagine(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.IMAGINE, doing),
                subject, obj, ActType.THINK)

    def isa(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.ISA, doing),
                subject, obj, ActType.BE)

    def laugh(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.LAUGH, doing),
                subject, obj, ActType.ACT)

    def look(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.LOOK, doing),
                subject, obj, ActType.LOOK)

    def make(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.MAKE, doing),
                subject, obj, ActType.ACT)

    def move(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.MOVE, doing),
                subject, obj, ActType.MOVE)

    def nod(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.NOD, doing),
                subject, obj, ActType.ACT)

    def notice(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.NOTICE, doing),
                subject, obj, ActType.THINK)

    def obtain(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.OBTAIN, doing),
                subject, obj, ActType.HAVE)

    def peep(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.PEEP, doing),
                subject, obj, ActType.LOOK)

    def puton(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.PUTON, doing),
                subject, obj, ActType.ACT)

    def read(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.READ, doing),
                subject, obj, ActType.ACT)

    def refuse(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.REFUSE, doing),
                subject, obj, ActType.ACT)

    def remember(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.REMEMBER, doing),
                subject, obj, ActType.THINK)

    def reply(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.REPLY, doing),
                subject, obj, ActType.TALK)

    def run(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.RUN, doing),
                subject, obj, ActType.MOVE)

    def sad(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.SAD, doing),
                subject, obj, ActType.THINK)

    def sit(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.SIT, doing),
                subject, obj, ActType.ACT)

    def sleep(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.SLEEP, doing),
                subject, obj, ActType.BE)

    def takeoff(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.TAKEOFF, doing),
                subject, obj, ActType.ACT)

    def tears(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.TEARS, doing),
                subject, obj, ActType.BE)

    def think(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.THINK, doing),
                subject, obj, ActType.THINK)

    def walk(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.WALK, doing),
                subject, obj, ActType.MOVE)

    def wear(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.WEAR, doing),
                subject, obj, ActType.ACT)

    def wonder(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.WONDER, doing),
                subject, obj, ActType.THINK)

    def write(self, obj: str="", doing: str=None,
                subject: Optional[Person]=None) -> Action: # pragma: no cover
        return self.do(Writer._validatedDoing(Does.WRITE, doing),
                subject, obj, ActType.ACT)

    ## privates
    def _validatedSubject(self, subject) -> (Person, Who):
        return subject if subject and isinstance(subject, (Person, Who)) else self.subject

    def _validatedDoing(base: Does, doing: Optional[str]) -> str:
        return base.value if not doing else doing
