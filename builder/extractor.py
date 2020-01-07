# -*- coding: utf-8 -*-
"""Define tool for extract
"""
## public libs
from itertools import chain
from typing import Any, Optional, Tuple, Union
## local libs
from utils import assertion
from utils.util_str import containsWordsIn
## local files
from builder.action import Action
from builder.block import Block
from builder.chapter import Chapter
from builder.day import Day
from builder.episode import Episode
from builder.item import Item
from builder.metadata import MetaData
from builder.person import Person
from builder.pronoun import Who
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word


## define types
StoryLike = (Story, Chapter, Episode, Scene, Action)
WordLike = (str, list, tuple)
U_Subjects = Union[Person, Stage, Day, Time, Item, Word]


## define class
class Extractor(object):
    """The tool class for extract
    """

    ## methods (container)
    @classmethod
    def actionsFrom(cls, src: StoryLike) -> Tuple[Union[Action, Block], ...]:
        if isinstance(src, Action):
            return (src,)
        else:
            return tuple(chain.from_iterable([sc.data for sc in cls.scenesFrom(src)]))

    @classmethod
    def chaptersFrom(cls, src: (Story, Chapter)) -> Tuple[Chapter, ...]:
        if isinstance(src, Chapter):
            return (src,)
        else:
            return assertion.isInstance(src, Story).data

    @classmethod
    def episodesFrom(cls, src: (Story, Chapter, Episode)) -> Tuple[Episode, ...]:
        if isinstance(src, Episode):
            return (src,)
        elif isinstance(src, Chapter):
            return src.data
        else:
            return tuple(chain.from_iterable([ch.data for ch in cls.chaptersFrom(src)]))

    @classmethod
    def scenesFrom(cls, src: StoryLike) -> Tuple[Scene, ...]:
        if isinstance(src, Scene):
            return (src,)
        elif isinstance(src, Episode):
            return src.data
        else:
            return tuple(chain.from_iterable([ep.data for ep in cls.episodesFrom(src)]))

    @classmethod
    def storyFrom(cls, src: Story) -> Story:
        return assertion.isInstance(src, Story)

    ## methods (data)
    @classmethod
    def daysFrom(cls, src: StoryLike) -> Tuple[Day, ...]:
        return cls._someObjectsFrom(src, Day)

    @classmethod
    def directionsFrom(cls, src: StoryLike) -> Tuple[Any, ...]:
        return tuple(chain.from_iterable([ac.data for ac in cls.actionsFrom(src)]))

    @classmethod
    def itemsFrom(cls, src: StoryLike) -> Tuple[Item, ...]:
        return cls._someObjectsFrom(src, Item)

    @classmethod
    def metadataFrom(cls, src: StoryLike) -> Tuple[MetaData, ...]:
        return cls._someObjectsFrom(src, MetaData)

    @classmethod
    def objectsFrom(cls, src: StoryLike) -> Tuple[U_Subjects, ...]:
        return cls._someObjectsFrom(src,
                (Person, Stage, Day, Time, Item, Word))

    @classmethod
    def personsFrom(cls, src: StoryLike) -> Tuple[Person, ...]:
        return cls._someObjectsFrom(src, Person)

    @classmethod
    def personAndSubjectsFrom(cls, src: StoryLike) -> Tuple[Person, ...]:
        persons = cls.personsFrom(src)
        subjects = cls.subjectsWithoutWhoFrom(src)
        return tuple(set(persons) | set(subjects))
    @classmethod
    def stagesFrom(cls, src: StoryLike) -> Tuple[Stage, ...]:
        return cls._someObjectsFrom(src, Stage)

    @classmethod
    def stringsFrom(cls, src: StoryLike) -> Tuple[str, ...]:
        return cls._someObjectsFrom(src, str)

    @classmethod
    def subjectsFrom(cls, src: StoryLike) -> Tuple[U_Subjects, ...]:
        return tuple(v.subject for v in cls.actionsFrom(src))

    @classmethod
    def subjectsWithoutWhoFrom(cls, src: StoryLike) -> Tuple[U_Subjects, ...]:
        return tuple(v.subject for v in cls.actionsFrom(src) if not isinstance(v.subject, Who))

    @classmethod
    def timesFrom(cls, src: StoryLike) -> Tuple[Time, ...]:
        return cls._someObjectsFrom(src, Time)

    @classmethod
    def wordsFrom(cls, src: StoryLike) -> Tuple[Word, ...]:
        return cls._someObjectsFrom(src, Word)

    @classmethod
    def _someObjectsFrom(cls, src: StoryLike, target: Any) -> Tuple[Any, ...]:
        return tuple(v for v in cls.directionsFrom(src) if isinstance(v, target))

