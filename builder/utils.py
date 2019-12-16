# -*- coding: utf-8 -*-
"""Define utility methods
"""
from typing import Any
from . import assertion
from .action import Action, ActType
from .chapter import Chapter
from .description import Description, DescType
from .episode import Episode
from .flag import Flag, NoFlag, NoDeflag
from .person import Person
from .scene import Scene
from .story import Story


def flagsSorted(data: list) -> list:
    tmp = []
    flags = [v for v in data if not v.isDeflag]
    deflags = [v for v in data if v.isDeflag]
    flags_names = sorted(set(v.info for v in flags if not isinstance(v, (NoFlag, NoDeflag))))
    deflags_names = sorted(set(v.info for v in deflags if not isinstance(v, (NoFlag, NoDeflag))))
    for v in flags_names:
        for f in flags:
            if v == f.info:
                tmp.append(f)
                break
    for v in deflags_names:
        for f in deflags:
            if v == f.info:
                tmp.append(f)
                break
    return tmp

def hasTrueList(li: list, fnc, *args) -> bool:
    return len([v for v in li if fnc(v, *args)]) > 0

def isDialogue(action: Action) -> bool:
    return action.act_type is ActType.TALK or action.description.desc_type is DescType.DIALOGUE

def personsSorted(data: list) -> list:
    tmp = []
    names = sorted(set(v.name for v in data))
    for v in names:
        for p in data:
            if v == p.name:
                tmp.append(p)
                break
    return tmp

def strOfDescription(action: Action, splitter: str="") -> str:
    return f"{splitter}".join(assertion.is_instance(action, Action).description.descs)

def toSomething(slf, *args, storyFnc, chapterFnc, episodeFnc, sceneFnc,
        src=None) -> (Story, Chapter, Episode, Scene):
    assert hasattr(slf, "src")
    _src = src if src else slf.src
    if isinstance(_src, Story):
        return storyFnc(_src, *args)
    elif isinstance(_src, Chapter):
        return chapterFnc(_src, *args)
    elif isinstance(_src, Episode):
        return episodeFnc(_src, *args)
    elif isinstance(_src, Scene):
        return sceneFnc(_src, *args)
    else:
        raise AssertionError("Non-reachable value: ", _src)

