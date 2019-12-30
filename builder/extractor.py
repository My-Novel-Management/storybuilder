# -*- coding: utf-8 -*-
"""Define tool for extract
"""
## public libs
from itertools import chain
from typing import Optional, Tuple, Union
## local libs
from utils import assertion
from utils.util_compare import equalsData
from utils.util_str import containsWordsIn
from utils.util_tools import toSomething
## local files
from builder.action import Action
from builder.chapter import Chapter
from builder.datapack import DataPack, titlePacked
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


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
    def alldirections(self) -> Tuple[Union[str, Shot], ...]:
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
        res.append(DataPack(f"{act.subject.name}:{act.doing}", "/".join(tmp)))
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
