# -*- coding: utf-8 -*-
"""Define utility for general.
"""
## public libs
from typing import Any, Callable
## local libs
from utils import assertion
## local files
from builder.chapter import Chapter
from builder.episode import Episode
from builder.scene import Scene
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


## methods (converter)
def tupleFiltered(origin: (list, tuple), filter_type: (object, tuple)) -> tuple:
    return tuple(v for v in origin if isinstance(v, filter_type))

def tupleEvenStr(val: (str, list, tuple)) -> tuple:
    if isinstance(val, str):
        return (val,)
    elif isinstance(val, tuple):
        return val
    else:
        return tuple(assertion.isList(val))

## methods (utility)
def toSomething(slf: object, *args: Any,
        storyFnc: Callable[[Story], Any],
        chapterFnc: Callable[[Chapter], Any],
        episodeFnc: Callable[[Episode], Any],
        sceneFnc: Callable[[Scene], Any],
        src=None) -> StoryLike:
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

def intCeiled(a: (int, float), b: (int, float)) -> int:
    return -(-assertion.isInt(a) // assertion.isInt(b))
