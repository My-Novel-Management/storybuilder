# -*- coding: utf-8 -*-
"""Define utility for compare
"""
## public libs
from typing import Tuple
## local libs
## local files
from builder.action import Action
from builder.basecontainer import BaseContainer
from builder.basedata import BaseData
from builder.block import Block
from builder.chapter import Chapter
from builder.day import Day
from builder.episode import Episode
from builder.item import Item
from builder.person import Person
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word


## methods
def equalsData(a: (Person, Stage, Day, Time, Item, Word),
        b: (Person, Stage, Day, Time, Item, Word)) -> bool:
    return type(a) is type(b) and _equalsBaseData(a, b)

def equalsContainers(a: (Story, Chapter, Episode, Scene), b: (Story, Chapter, Episode, Scene)) -> bool:
    return type(a) is type(b) and _equalsBaseContainer(a, b)

def equalsContainerLists(alist: tuple, blist: tuple) -> bool:
    for a,b in zip(alist, blist):
        if not equalsContainers(a, b):
            return False
    return True


## privates
def _equalsBaseContainer(a: BaseContainer, b: BaseContainer) -> bool:
    return a.title == b.title and len(a.data) == len(b.data) and len(a.data[0]) == len(b.data[0]) and a.priority == b.priority

def _equalsBaseData(a: BaseData, b: BaseData) -> bool:
    return a.name == b.name and len(a.data) == len(b.data) and len(a.data[0]) == len(b.data[0])
