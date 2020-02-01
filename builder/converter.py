# -*- coding: utf-8 -*-
"""Define tool for convert.
"""
## public libs
from itertools import chain
from typing import Tuple
## local libs
from utils import assertion
from utils.util_str import dictCombined, strReplacedTagByDict, strDuplicatedChopped
## local files
from builder import __PRIORITY_MAX__, __PRIORITY_MIN__, __PRIORITY_NORMAL__
from builder import __CONTINUED__
from builder import ActType, MetaType, TagType
from builder.action import Action
from builder.area import Area
from builder.basedata import BaseData
from builder.block import Block
from builder.chapter import Chapter
from builder.episode import Episode
from builder.extractor import Extractor
from builder.metadata import MetaData
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
    def areasOrdered(cls, basepoint: Area, src: StoryLike) -> list:
        tmp = []
        for v in set(Extractor.areasFrom(src)):
            tmp.append((v, basepoint.distance(v)))
        tmp1 = dict(tmp)
        return [v for v in dict(sorted(tmp1.items(), key=lambda x: x[1])).keys()]

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
    def srcContinuedActionDeveloped(cls, src: StoryLike) -> StoryLike:
        if isinstance(src, Scene):
            tmp = []
            acttype = ActType.ACT
            tagtype = TagType.NONE
            subject = Who()
            for ac in src.data:
                if ActType.META is ac.act_type and TagType.COMMAND is ac.tag_type and __CONTINUED__ == ac.note:
                    tmp.append(Action(*ac.data, subject=subject, act_type=acttype, tag_type=tagtype))
                else:
                    acttype = ac.act_type
                    tagtype = ac.tag_type
                    subject = ac.subject
                    tmp.append(ac)
            return src.inherited(*tmp)
        else:
            return src.inherited(*[cls.srcContinuedActionDeveloped(v) for v in src.data])

    @classmethod
    def sceneSettingPronounReplaced(cls, src: Story, areas: dict) -> Story:
        tmp = []
        camera, area, stage, day, time = None, Area.getDefault(), None, None, None
        for ch in src.data:
            tmpEpisodes = []
            for ep in ch.data:
                tmpScenes = []
                for sc in ep.data:
                    _stage = stage if isinstance(sc.stage, Where) else sc.stage
                    _area = area if isinstance(sc.area, Where) else sc.area
                    if _stage.area and _stage.area in areas:
                        _area = areas[_stage.area]
                    tmpS = sc.inherited(*sc.data,
                            camera=camera if isinstance(sc.camera, Who) else sc.camera,
                            area=_area,
                            stage=_stage,
                            day=day if isinstance(sc.day, When) else sc.day,
                            time=time if isinstance(sc.time, When) else sc.time)
                    camera, area, stage, day, time = tmpS.camera, tmpS.area, tmpS.stage, tmpS.day, tmpS.time
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
            return action, action.subject

    @classmethod
    def actionDividedFrom(cls, src: StoryLike) -> StoryLike:
        if isinstance(src, Scene):
            tmp = []
            for ac in src.data:
                if ac.act_type in (ActType.ACT, ActType.LOOK, ActType.TALK, ActType.VOICE, ActType.EXPLAIN, ActType.THINK):
                    dires = Extractor.directionsFrom(ac)
                    strs = [v for v in dires if isinstance(v, str)]
                    others = [v for v in dires if not isinstance(v, str)]
                    descs = [strDuplicatedChopped(f"{v}。") for v in list(chain.from_iterable(v.split("。") for v in strs)) if v]
                    descs = [strDuplicatedChopped(f"{v}、") for v in list(chain.from_iterable(v.split("、") for v in descs)) if v]
                    cnt = 0
                    _others = []
                    for v in descs:
                        if cnt == 0:
                            _others = others
                        elif len(descs)  - 1 > cnt:
                            _others = ["&"]
                        else:
                            _others = ""
                        cnt += 1
                        tmp.append(Action(v, *_others,
                            subject=ac.subject,
                            act_type=ac.act_type,
                            tag_type=ac.tag_type,
                            itemCount=ac.itemCount,
                            note=ac.note,
                            priority=ac.priority,
                            ))
                else:
                    tmp.append(ac)
            return src.inherited(*tmp)
        else:
            return src.inherited(*[cls.actionDividedFrom(v) for v in src.data])

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
        if isinstance(dire, MetaData):
            return MetaData(dire.data, title=cls.directionReplacedTags(dire.name, tags, prefix, camera, subject),
                    note=cls.directionReplacedTags(dire.note, tags, prefix, camera, subject))
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
    def sceneFromBlock(cls, src: Block) -> Scene:
        return Scene(src.title, *src.data,
                camera=src.data[0].subject)

    @classmethod
    def srcExpandBlocks(cls, src: StoryLike) -> StoryLike:
        def _blockPacked(block: Block):
            return (Action(MetaData(MetaType.BLOCK_START, title=block.title),act_type=ActType.META),) + block.data + (Action(MetaData(MetaType.BLOCK_END, title=block.title),act_type=ActType.META),)
        if isinstance(src, Scene):
            return src.inherited(
                    *list(chain.from_iterable(
                        [[v] if isinstance(v, Action) else _blockPacked(v) for v in src.data])))
        else:
            return src.inherited(*[cls.srcExpandBlocks(v) for v in src.data])

    @classmethod
    def srcReducedByChapter(cls, src: Story, start: int, end: int) -> Story:
        tmp = []
        idx = 0
        for ch in src.data:
            if idx >= start and (idx <= end or end < 0):
                tmp.append(ch)
            idx += 1
        return src.inherited(*tmp)

    @classmethod
    def srcReducedByEpisode(cls, src: Story, start: int, end: int) -> Story:
        tmp = []
        idx = 0
        for ch in src.data:
            eps = []
            for ep in ch.data:
                if idx >= start and (idx <= end or end < 0):
                    eps.append(ep)
                idx += 1
            tmp.append(ch.inherited(*eps))
        return src.inherited(*tmp)
