# -*- coding: utf-8 -*-
"""Define tool for extract
"""
## public libs
from itertools import chain
from typing import Any, Optional, Tuple, Union
## local libs
from utils import assertion
from utils.util_compare import equalsData
from utils.util_str import containsWordsIn
from utils.util_tools import toSomething
## local files
from builder.action import Action
from builder.chapter import Chapter
from builder.datapack import DataPack, titlePacked
from builder.day import Day
from builder.episode import Episode
from builder.item import Item
from builder.person import Person
from builder.scene import Scene
from builder.shot import Shot
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word


## define types
StoryLike = (Story, Chapter, Episode, Scene)
WordLike = (str, list, tuple)

class Extractor(object):
    """The tool class for extract
    """
    __NO_DATA__ = "__no_data__"

    def __init__(self, src: StoryLike):
        self._src = assertion.isInstance(src, StoryLike)

    ## property
    @property
    def src(self) -> StoryLike:
        return self._src

    @property
    def story(self) -> Story:
        return self._src if isinstance(self._src, Story) else Story(self.__NO_DATA__)

    @property
    def chapters(self) -> Tuple[Chapter, ...]:
        if isinstance(self._src, (Episode, Scene)):
            return ()
        elif isinstance(self._src, Chapter):
            return (self._src,)
        else:
            return self.story.chapters

    @property
    def episodes(self) -> Tuple[Episode, ...]:
        if isinstance(self._src, Scene):
            return ()
        elif isinstance(self._src, Episode):
            return (self._src,)
        else:
            return tuple(chain.from_iterable(v.episodes for v in self.chapters))

    @property
    def scenes(self) -> Tuple[Scene, ...]:
        if isinstance(self._src, Scene):
            return (self._src,)
        else:
            return tuple(chain.from_iterable(v.scenes for v in self.episodes))

    @property
    def actions(self) -> Tuple[Action, ...]:
        return tuple(chain.from_iterable(v.actions for v in self.scenes))

    @property
    def alldirections(self) -> Tuple[Union[str, Shot, Person, Stage, Day, Time, Item, Word], ...]:
        return tuple(chain.from_iterable(v.acts for v in self.actions))

    @property
    def directions(self) -> Tuple[str, ...]:
        return tuple(v for v in self.alldirections if not isinstance(v, Shot))

    @property
    def shots(self) -> Tuple[Shot, ...]:
        return tuple(v for v in self.alldirections if isinstance(v, Shot))

    @property
    def persons(self) -> Tuple[Person, ...]:
        return tuple(v.subject for v in self.actions if isinstance(v.subject, Person))

    @property
    def stages(self) -> Tuple[Stage, ...]:
        return tuple(v for v in self.alldirections if isinstance(v, Stage)) \
                + tuple(v.camera for v in self.scenes)

    @property
    def days(self) -> Tuple[Day, ...]:
        return tuple(v for v in self.alldirections if isinstance(v, Day)) \
                + tuple(v.day for v in self.scenes)

    @property
    def times(self) -> Tuple[Time, ...]:
        return tuple(v for v in self.alldirections if isinstance(v, Time)) \
                + tuple(v.time for v in self.scenes)

    @property
    def items(self) -> Tuple[Item, ...]:
        return tuple(v for v in self.alldirections if isinstance(v, Item))

    @property
    def words(self) -> Tuple[Word, ...]:
        return tuple(v for v in self.alldirections if isinstance(v, Word))

    ## methods
    def descsHasWord(self, words: dict, src: StoryLike=None) -> Tuple[DataPack, ...]:
        return toSomething(self,
                words,
                storyFnc=_descsHasWordIn,
                chapterFnc=_descsHasWordInChapter,
                episodeFnc=_descsHasWordInEpisode,
                sceneFnc=_descsHasWordInScene,
                src=src if src else self.src)

    def dialoguesOfPerson(self, person: Person, src: StoryLike=None) -> Tuple[DataPack, ...]:
        return toSomething(self,
                person,
                storyFnc=_dialoguesOfPersonIn,
                chapterFnc=_dialoguesOfPersonInChapter,
                episodeFnc=_dialoguesOfPersonInEpisode,
                sceneFnc=_dialoguesOfPersonInScene,
                src=src if src else self.src)

    def getChapter(self, num: int=0) -> Optional[Chapter]:
        if num < len(self.chapters):
            return self.chapters[num]
        else:
            return None

    def getEpisode(self, num: int=0) -> Optional[Episode]:
        if num < len(self.episodes):
            return self.episodes[num]
        else:
            return None

    def getScene(self, num: int=0) -> Optional[Scene]:
        if num < len(self.scenes):
            return self.scenes[num]
        else:
            return None

    ## from world
    @classmethod
    def getDaysFromWorld(cls, src: dict) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, Day)])

    @classmethod
    def getItemsFromWorld(cls, src: dict) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, Item)])

    @classmethod
    def getPersonsFromWorld(cls, src: dict) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, Person)])

    @classmethod
    def getStagesFromWorld(cls, src: dict) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, Stage)])

    @classmethod
    def getTimesFromWorld(cls, src: dict) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, Time)])

    @classmethod
    def getWordsFromWorld(cls, src: dict) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, Word)])

    @classmethod
    def getShotsFrom(cls, act: Action) -> tuple:
        return tuple(v for v in act.acts if isinstance(v, Shot))

    @classmethod
    def getAllDirectionsFrom(cls, act: Action) -> tuple:
        return tuple(v for v in act.acts)

    @classmethod
    def getDirectionsFrom(cls, act: Action) -> tuple:
        return tuple(v for v in act.acts if isinstance(v, str))

    @classmethod
    def getObjectsFrom(vls, act: Action) -> tuple:
        return tuple(v for v in act.acts if not isinstance(v, (str, Shot)))

## privates
''' descs has word
'''
def _descsHasWordIn(story: Story, words: WordLike) -> Tuple[DataPack, ...]:
    return (titlePacked(story),) + tuple(
            chain.from_iterable(_descsHasWordInChapter(v, words) for v in story.chapters))

def _descsHasWordInChapter(chapter: Chapter, words: WordLike) -> Tuple[DataPack, ...]:
    return (titlePacked(chapter),) + tuple(
            chain.from_iterable(_descsHasWordInEpisode(v, words) for v in chapter.episodes))

def _descsHasWordInEpisode(episode: Episode, words: WordLike) -> Tuple[DataPack, ...]:
    return (titlePacked(episode),) + tuple(
            chain.from_iterable(_descsHasWordInScene(v, words) for v in episode.scenes))

def _descsHasWordInScene(scene: Scene, words: WordLike) -> Tuple[DataPack, ...]:
    res = []
    for act in scene.actions:
        tmp = []
        for shot in [v for v in act.acts if isinstance(v, Shot)]:
            for info in shot.infos:
                if containsWordsIn(info, words):
                    tmp.append(info)
        res.append(DataPack(f"{act.subject.name}:{act.act_type.name}", "/".join(tmp)))
    return (titlePacked(scene),) + tuple(res)

''' dialogues of person
'''
def _dialoguesOfPersonIn(story: Story, person: Person) -> Tuple[DataPack, ...]:
    return (titlePacked(story),) + tuple(
            chain.from_iterable(_dialoguesOfPersonInChapter(v, person) for v in story.chapters))

def _dialoguesOfPersonInChapter(chapter: Chapter, person: Person) -> Tuple[DataPack, ...]:
    return (titlePacked(chapter),) + tuple(
            chain.from_iterable(_dialoguesOfPersonInEpisode(v, person) for v in chapter.episodes))

def _dialoguesOfPersonInEpisode(episode: Episode, person: Person) -> Tuple[DataPack, ...]:
    return (titlePacked(episode),) + tuple(
            chain.from_iterable(_dialoguesOfPersonInScene(v, person) for v in episode.scenes))

def _dialoguesOfPersonInScene(scene: Scene, person: Person) -> Tuple[DataPack, ...]:
    res = []
    for act in scene.actions:
        if equalsData(act.subject, person):
            for shot in [v for v in act.acts if isinstance(v, Shot)]:
                res.append(DataPack("dialogue", "/".join(v for v in shot.infos)))
    return (titlePacked(scene),) + tuple(res)
