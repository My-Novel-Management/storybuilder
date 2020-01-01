# -*- coding: utf-8 -*-
"""Define tool for convert.
"""
## public libs
from itertools import chain
from typing import Tuple
## local libs
from utils import assertion
from utils.util_str import strReplacedTagByDict, strDividedBySplitter
from utils.util_tools import toSomething
## local files
from builder import __PRIORITY_MAX__, __PRIORITY_MIN__, __PRIORITY_NORMAL__
from builder import TagType
from builder.action import Action
from builder.block import Block
from builder.chapter import Chapter
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story
from builder.when import When
from builder.where import Where
from builder.who import Who


## define typees
StoryLike = (Story, Chapter, Episode, Scene, Action)

class Converter(object):
    """Tool for convert
    """
    def __init__(self, src: StoryLike):
        self._src = assertion.isInstance(src, StoryLike)

    ## property
    @property
    def src(self) -> StoryLike:
        return self._src

    ## methods
    def srcFilterByPriority(self, priority: int=__PRIORITY_NORMAL__, src: StoryLike=None) -> StoryLike:
        return toSomething(self,
                priority,
                storyFnc=_storyFilterByPriority,
                chapterFnc=_chapterFilterByPriority,
                episodeFnc=_episodeFilterByPriority,
                sceneFnc=_sceneFilterByPriority,
                src=src if src else self.src)

    def srcReplacedPronouns(self, src: StoryLike=None) -> StoryLike:
        return toSomething(self,
                storyFnc=_storyReplacedPronouns,
                chapterFnc=_chapterReplacedPronouns,
                episodeFnc=_episodeReplacedPronouns,
                sceneFnc=_sceneReplacedPronouns,
                src=src if src else self.src)

    def srcReplacedTags(self, tags: dict, prefix: str, src: StoryLike=None) -> StoryLike:
        return toSomething(self,
                tags, prefix,
                storyFnc=_storyReplacedTags,
                chapterFnc=_chapterReplacedTags,
                episodeFnc=_episodeReplacedTags,
                sceneFnc=_sceneReplacedTags,
                src=src if src else self.src)

    def srcSerialized(self, src: StoryLike=None) -> StoryLike:
        return toSomething(self,
                storyFnc=_storySerialized,
                chapterFnc=_chapterSerialized,
                episodeFnc=_episodeSerialized,
                sceneFnc=_sceneSerialized,
                src=src if src else self.src)

    ## utility
    @classmethod
    def personNamesConstructed(cls, src: Person) -> tuple:
        tmp = src.fullname if src.fullname else src.name
        last, first = strDividedBySplitter(tmp, ",")
        full = tmp.replace(',', '')
        exfull = src.name
        if src.fullname:
            exfull = f"{first}・{last}"
        return (last, first, full, exfull)

## privates (filter)
''' filter by priority
'''
def _storyFilterByPriority(story: Story, priority: int) -> Story:
    return story.inherited(*[_chapterFilterByPriority(v, priority) for v in story.chapters if v.priority >= priority])

def _chapterFilterByPriority(chapter: Chapter, priority: int) -> Chapter:
    return chapter.inherited(*[_episodeFilterByPriority(v, priority) for v in chapter.episodes if v.priority >= priority])

def _episodeFilterByPriority(episode: Episode, priority: int) -> Episode:
    return episode.inherited(*[_sceneFilterByPriority(v, priority) for v in episode.scenes if v.priority >= priority])

def _sceneFilterByPriority(scene: Scene, priority: int) -> Scene:
    return scene.inherited(*[v for v in scene.actions if v.priority >= priority])

## privates (replacement)
''' replace pronouns
'''
def _storyReplacedPronouns(story: Story) -> Story:
    return story.inherited(*[_chapterReplacedPronouns(v) for v in story.chapters])

def _chapterReplacedPronouns(chapter: Chapter) -> Chapter:
    return chapter.inherited(*[_episodeReplacedPronouns(v) for v in chapter.episodes])

def _episodeReplacedPronouns(episode: Episode) -> Episode:
    tmp = []
    camera = Person.getGod()
    stage, day, time = None, None, None
    for v in episode.scenes:
        sc = v.inherited(*v.actions,
                camera=camera if isinstance(v.camera, Who) else v.camera,
                stage=stage if isinstance(v.stage, Where) else v.stage,
                day=day if isinstance(v.day, When) else v.day,
                time=time if isinstance(v.time, When) else v.time)
        camera = sc.camera
        stage = sc.stage
        day = sc.day
        time = sc.time
        tmp.append(_sceneReplacedPronouns(sc))
    return episode.inherited(*tmp)

def _sceneReplacedPronouns(scene: Scene) -> Scene:
    tmp = []
    cur = scene.camera
    for v in scene.actions:
        if not v.tag_type is TagType.NONE:
            tmp.append(v)
        else:
            act = _actionReplacedPronouns(v, cur)
            cur = act.subject
            tmp.append(act)
    return scene.inherited(*tmp)

def _actionReplacedPronouns(action: Action, current: Person) -> Action:
    if not action.tag_type is TagType.NONE:
        return action
    elif isinstance(action.subject, Who):
        tmp = action.inherited(*action.acts, subject=current)
        return tmp
    else:
        return action

''' replace tags
'''
def _storyReplacedTags(story: Story, tags: dict, prefix: str) -> Story:
    return story.inherited(*[_chapterReplacedTags(v, tags, prefix) for v in story.chapters],
        title=strReplacedTagByDict(story.title, tags, prefix))

def _chapterReplacedTags(chapter: Chapter, tags: dict, prefix: str) -> Chapter:
    return chapter.inherited(*[_episodeReplacedTags(v, tags, prefix) for v in chapter.episodes],
        title=strReplacedTagByDict(chapter.title, tags, prefix))

def _episodeReplacedTags(episode: Episode, tags: dict, prefix: str) -> Episode:
    return episode.inherited(*[_sceneReplacedTags(v, tags, prefix) for v in episode.scenes],
            title=strReplacedTagByDict(episode.title, tags, prefix))

def _sceneReplacedTags(scene: Scene, tags: dict, prefix: str) -> Scene:
    return scene.inherited(*[_actionReplacedTags(v, tags, prefix, scene.camera) for v in scene.actions],
            title=strReplacedTagByDict(scene.title, tags, prefix))

def _actionReplacedTags(action: Action, tags: dict, prefix: str, camera: Person) -> Action:
    def _containsPrefix(vals, pref):
        for v in vals:
            if isinstance(v, Shot):
                for x in v.infos:
                    if pref in x:
                        return True
            elif isinstance(v, str):
                if pref in v:
                    return True
            else:
                if pref in v.name:
                    return True
        return False
    if not action.tag_type is TagType.NONE:
        if action.tag_type in (TagType.COMMENT, TagType.TITLE):
            return action.inherited(
                    note=strReplacedTagByDict(action.note, tags, prefix),
                    )
        else:
            return action
    elif not _containsPrefix(action.acts, prefix):
        return action
    else:
        return action.inherited(
                *[_shotReplacedTags(v, action.subject, tags, prefix, camera) if isinstance(v, Shot) else _docReplacedTags(v, action.subject, tags, prefix, camera) for v in action.acts]
                )

def _shotReplacedTags(shot: Shot, subject: Person,tags: dict, prefix: str, camera: Person) -> Shot:
    tmp = []
    for v in shot.infos:
        tmp.append(_docReplacedTags(v, subject, tags, prefix, camera))
    return shot.inherited(*tmp)

def _docReplacedTags(val: str, subject: Person, tags: dict, prefix: str, camera: Person) -> str:
    tmp = val
    if hasattr(subject, "calling"):
        tmp = strReplacedTagByDict(tmp, subject.calling, prefix)
    calling = {**camera.calling, **{"CS":camera.calling["S"], "CM":camera.calling["M"]}}
    tmp = strReplacedTagByDict(tmp, calling, prefix)
    tmp = strReplacedTagByDict(tmp, tags, prefix)
    if prefix in tmp:
        AssertionError(f"Cannot convert tag in {tmp}")
    return tmp

''' expand block to actions
'''
def _storySerialized(story: Story) -> Story:
    return story.inherited(*[_chapterSerialized(v) for v in story.chapters])

def _chapterSerialized(chapter: Chapter) -> Chapter:
    return chapter.inherited(*[_episodeSerialized(v) for v in chapter.episodes])

def _episodeSerialized(episode: Episode) -> Episode:
    return episode.inherited(*[_sceneSerialized(v) for v in episode.scenes])

def _sceneSerialized(scene: Scene) -> Scene:
    tmp = list(chain.from_iterable(
        [[v] if isinstance(v, Action) else v.acts for v in scene.actions]))
    return scene.inherited(*tmp)

