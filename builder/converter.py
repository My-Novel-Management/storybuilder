# -*- coding: utf-8 -*-
"""Define tool for convert.
"""
## public libs
from itertools import chain
from typing import Tuple
## local libs
from utils import assertion
from utils.util_str import dictCombined, strReplacedTagByDict
## local files
from builder import __PRIORITY_MAX__, __PRIORITY_MIN__, __PRIORITY_NORMAL__
from builder import TagType
from builder.action import Action
from builder.basedata import BaseData
from builder.block import Block
from builder.chapter import Chapter
from builder.episode import Episode
from builder.person import Person
from builder.scene import Scene
from builder.story import Story
from builder.pronoun import When, Where, Who


## define typees
StoryLike = (Story, Chapter, Episode, Scene, Action)


## define class
class Converter(object):
    """Tool for convert
    """
    ## methods
    @classmethod
    def srcFilterByPriority(cls, src: StoryLike, priority: int=__PRIORITY_NORMAL__) -> StoryLike:
        if isinstance(src, Scene):
            return src.inherited(*[ac for ac in src.data if ac.priority >= priority])
        else:
            return src.inherited(*[cls.srcFilterByPriority(v, priority) for v in src.data if v.priority >= priority])

    @classmethod
    def srcPronounsReplaced(cls, src: StoryLike) -> StoryLike:
        if isinstance(src, Scene):
            tmp = []
            cur = src.camera
            for v in src.data:
                act, cur = cls.actionReplacedPronoun(v, cur)
                tmp.append(act)
            return src.inherited(*tmp)
        else:
            return src.inherited(*[cls.srcPronounsReplaced(v) for v in src.data])

    @classmethod
    def sceneSettingPronounReplaced(cls, src: Story) -> Story:
        tmp = []
        camera, stage, day, time = None, None, None, None
        for ch in src.data:
            tmpEpisodes = []
            for ep in ch.data:
                tmpScenes = []
                for sc in ep.data:
                    tmpS = sc.inherited(*sc.data,
                            camera=camera if isinstance(sc.camera, Who) else sc.camera,
                            stage=stage if isinstance(sc.stage, Where) else sc.stage,
                            day=day if isinstance(sc.day, When) else sc.day,
                            time=time if isinstance(sc.time, When) else sc.time)
                    camera, stage, day, time = tmpS.camera, tmpS.stage, tmpS.day, tmpS.time
                    tmpScenes.append(tmpS)
                tmpEpisodes.append(ep.inherited(*tmpScenes))
            tmp.append(ch.inherited(*tmpEpisodes))
        return src.inherited(*tmp)

    @classmethod
    def actionReplacedPronoun(cls, action: Action, current: Person) -> Tuple[Action, Person]:
        if not action.tag_type is TagType.NONE:
            return action, current
        elif isinstance(action.subject, Who):
            tmp = action.inherited(*action.data, subject=current)
            return tmp, current
        else:
            cur = action.subject if isinstance(current, Who) else current
            return action, cur

    @classmethod
    def srcReplacedTags(cls, src: StoryLike, tags: dict, prefix: str) -> StoryLike:
        if isinstance(src, Scene):
            return src.inherited(
                    *[cls.actionReplacedTags(v, tags, prefix, src.camera) for v in src.data],
                    title=strReplacedTagByDict(src.title, tags, prefix),
                    note=strReplacedTagByDict(src.note, tags, prefix))
        else:
            return src.inherited(*[cls.srcReplacedTags(v, tags, prefix) for v in src.data],
                    title=strReplacedTagByDict(src.title, tags, prefix),
                        note=strReplacedTagByDict(src.note, tags, prefix))

    @classmethod
    def actionReplacedTags(cls, action: Action, tags: dict, prefix: str, camera: Person) -> Action:
        if not action.tag_type is TagType.NONE:
            return action.inherited(note=strReplacedTagByDict(action.note, tags, prefix))
        else:
            return action.inherited(
                    *[cls.directionReplacedTags(v, tags, prefix, camera,
                        action.subject) for v in action.data],
                    note=strReplacedTagByDict(action.note, tags, prefix))

    @classmethod
    def directionReplacedTags(cls, dire:(str,  BaseData), tags: dict, prefix: str,
            camera: Person, subject: Person) -> (str, BaseData):
        if not isinstance(dire, str):
            return dire
        tmp = dire
        if hasattr(subject, "calling"):
            tmp = strReplacedTagByDict(tmp, subject.calling, prefix)
        if hasattr(camera, "calling"):
            calling = dictCombined(camera.calling,
                {"CS":camera.calling["S"], "CM":camera.calling["M"]})
            tmp = strReplacedTagByDict(tmp, calling, prefix)
        tmp = strReplacedTagByDict(tmp, tags, prefix)
        if prefix in tmp:
            raise AssertionError(f"Cannot convert tag in {tmp}")
        return tmp

    @classmethod
    def srcExpandBlocks(cls, src: StoryLike) -> StoryLike:
        if isinstance(src, Scene):
            return src.inherited(
                    *list(chain.from_iterable(
                        [[v] if isinstance(v, Action) else v.data for v in src.data])))
        else:
            return src.inherited(*[cls.srcExpandBlocks(v) for v in src.data])

    @classmethod
    def srcReducedByChapter(cls, src: Story, start: int, end: int) -> Story:
        tmp = []
        idx = 0
        inEnabled = False
        for ch in src.data:
            if idx == start:
                inEnabled = True
            elif end > 0 and idx == end:
                inEnabled = False
            if inEnabled:
                tmp.append(ch)
            idx += 1
        return src.inherited(*tmp)

    @classmethod
    def srcReducedByEpisode(cls, src: Story, start: int, end: int) -> Story:
        tmp = []
        idx = 0
        inEnabled = False
        for ch in src.data:
            eps = []
            for ep in ch.data:
                if idx == start:
                    inEnabled = True
                elif end > 0 and idx == end:
                    inEnabled = False
                if inEnabled:
                    eps.append(ep)
                idx += 1
            tmp.append(ch.inherited(*eps))
        return src.inherited(*tmp)
