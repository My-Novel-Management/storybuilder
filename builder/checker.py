# -*- coding: utf-8 -*-
"""Define tool for check
"""
## public libs
## local libs
from utils import assertion
from utils.util_tools import toSomething
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.item import Item
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


class Checker(object):
    """The tool class for check
    """
    def __init__(self, src: StoryLike):
        self._src = assertion.isInstance(src, StoryLike)

    ## property
    @property
    def src(self) -> StoryLike:
        return self._src

    ## methods
    def objectInOut(self, src: StoryLike=None) -> bool:
        return toSomething(self,
                storyFnc=_objectInOutIn,
                chapterFnc=_objectInOutInChapter,
                episodeFnc=_objectInOutInEpisode,
                sceneFnc=_objectInOutInScene,
                src=src if src else self.src)


## privates
''' check object in-out
'''
def _objectInOutIn(story: Story) -> bool:
    return not len([v for v in story.chapters if not _objectInOutInChapter(v)]) > 0

def _objectInOutInChapter(chapter: Chapter) -> bool:
    return not len([v for v in chapter.episodes if not _objectInOutInEpisode(v)]) > 0

def _objectInOutInEpisode(episode: Episode) -> bool:
    return not len([v for v in episode.scenes if not _objectInOutInScene(v)]) > 0

def _objectInOutInScene(scene: Scene) -> bool:
    # TODO
    #   itemの管理
    tmp = {}
    msg = []
    isSucceeded = []
    def _addition(act: Action, name: str):
        if name in tmp:
            tmp[name] += int(act.note)
        else:
            tmp[name] = int(act.note)
        return True
    def _subtract(act: Action, name: str):
        if name in tmp:
            tmp[name] -= int(act.note)
            return True
        else:
            msg.append(f"Cannot find {name}, when {act.act_type.name}! in {scene.title}")
            return False
    for act in scene.actions:
        if not act.tag_type is TagType.NONE:
            continue
        ## exist
        elif act.act_type in (ActType.BE, ActType.COME):
            isSucceeded.append(_addition(act, act.subject.name))
        elif act.act_type in (ActType.DESTROY, ActType.GO):
            isSucceeded.append(_subtract(act, act.subject.name))
        ## control
        elif act.act_type in (ActType.HAVE, ActType.WEAR):
            items = [v for v in act.acts if isinstance(v, Item)]
            if act.subject.name in tmp:
                for v in items:
                    isSucceeded.append(_addition(act, v.name))
            else:
                msg.append(f"Cannot find {act.subject.name}, when {act.act_type.name}! in {scene.title}")
                isSucceeded.append(False)
        elif act.act_type in (ActType.DISCARD, ActType.TAKEOFF):
            items = [v for v in act.acts if isinstance(v, Item)]
            if act.subject.name in tmp:
                for v in items:
                    isSucceeded.append(_subtract(act, v.name))
            else:
                msg.append(f"Cannot find {act.subject.name}, when {act.act_type.name}! in {scene.title}")
                isSucceeded.append(False)
        ## basic
        elif act.act_type in (ActType.TALK, ActType.THINK, ActType.ACT, ActType.WEAR):
            if not act.subject.name in tmp:
                msg.append(f"Cannot find {act.subject.name}, when ACT! in {scene.title}")
                isSucceeded.append(False)
    if len([v for v in isSucceeded if not v]) > 0:
        for v in msg:
            print(v)
        return False
    else:
        return True
