# -*- coding: utf-8 -*-
"""Define tool for parser
"""
## public libs
from itertools import chain
from typing import Tuple
## local libs
from utils import assertion
from utils.util_str import strDuplicatedChopped
from utils.util_tools import toSomething
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.chapter import Chapter
from builder.datapack import DataPack, titlePacked
from builder.episode import Episode
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


class Parser(object):
    """The tool class for parser
    """
    def __init__(self, src: StoryLike):
        self._src = assertion.isInstance(src, StoryLike)

    ## property
    @property
    def src(self) -> StoryLike:
        return self._src

    ## methods
    def toContes(self, src: StoryLike=None) -> Tuple[DataPack, ...]:
        return toSomething(self,
                storyFnc=_toContesFrom,
                chapterFnc=_toContesFromChapter,
                episodeFnc=_toContesFromEpisode,
                sceneFnc=_toContesFromScene,
                src=src if src else self.src)

    def toDescriptions(self, src: StoryLike=None) -> Tuple[DataPack, ...]:
        return toSomething(self,
                storyFnc=_toDescsFrom,
                chapterFnc=_toDescsFromChapter,
                episodeFnc=_toDescsFromEpisode,
                sceneFnc=_toDescsFromScene,
                src=src if src else self.src)

    def toDescriptionsWithRubi(self, rubis: dict, src: StoryLike=None) -> Tuple[DataPack, ...]:
        tmp = self.toDescriptions(src)
        return _toDescsFromWithRubi(tmp, rubis)

    def toObjectMotions(self, src: StoryLike=None) -> tuple:
        return ()

    def toOutlines(self, src: StoryLike=None) -> Tuple[DataPack, ...]:
        return toSomething(self,
                storyFnc=_toOutlinesFrom,
                chapterFnc=_toOutlinesFromChapter,
                episodeFnc=_toOutlinesFromEpisode,
                sceneFnc=_toOutlinesFromScene,
                src=src if src else self.src)


## privates
''' to conte
'''
def _toContesFrom(story: Story) -> Tuple[DataPack, ...]:
    return (titlePacked(story),) + tuple(
            chain.from_iterable(_toContesFromChapter(v) for v in story.chapters))

def _toContesFromChapter(chapter: Chapter) -> Tuple[DataPack, ...]:
    return (titlePacked(chapter),) + tuple(
            chain.from_iterable(_toContesFromEpisode(v) for v in chapter.episodes))

def _toContesFromEpisode(episode: Episode) -> Tuple[DataPack, ...]:
    return (titlePacked(episode),) + tuple(
            chain.from_iterable(_toContesFromScene(v) for v in episode.scenes))

def _toContesFromScene(scene: Scene) -> Tuple[DataPack, ...]:
    tmp = []
    # TODO
    def _nameOf(v):
        if isinstance(v, str):
            return v
        else:
            return v.name
    for act in scene.actions:
        if act.act_type is ActType.TAG:
            # TODO
            continue
        elif act.act_type is ActType.TALK:
            desc = []
            for shot in [v for v in act.acts if isinstance(v, Shot)]:
                desc.append(_descFromShot(shot))
            actor = act.subject.name
            tmp.append(DataPack(f"{act.act_type.name}:{actor}",
                f"{act.doing}:" + "/".join(desc)))
        else:
            dires = [_nameOf(v) for v in act.acts if not isinstance(v, Shot)]
            actor = act.subject.name
            tmp.append(DataPack(f"{act.act_type.name}:{actor}",
                f"{act.doing}:" + "/".join(dires)))
    return (titlePacked(scene),
            DataPack("scene setting",
                ":".join([scene.camera.name,
                    scene.stage.name, scene.day.name, scene.time.name]))) + tuple(tmp)

''' to description
'''
def _toDescsFrom(story: Story) -> Tuple[DataPack, ...]:
    return (titlePacked(story),) + tuple(
            chain.from_iterable(_toDescsFromChapter(v) for v in story.chapters))

def _toDescsFromChapter(chapter: Chapter) -> Tuple[DataPack, ...]:
    return (titlePacked(chapter),) + tuple(
            chain.from_iterable(_toDescsFromEpisode(v) for v in chapter.episodes))

def _toDescsFromEpisode(episode: Episode) -> Tuple[DataPack, ...]:
    return (titlePacked(episode),) + tuple(
            chain.from_iterable(_toDescsFromScene(v) for v in episode.scenes))

def _toDescsFromScene(scene: Scene) -> Tuple[DataPack, ...]:
    tmp = []
    res = []
    inAct = False
    act_type = ActType.ACT
    def _actTypeStr(t: ActType):
        return "dialogue" if t is ActType.TALK else "desc"
    def _descCombined(t: ActType, v: list):
        return strDuplicatedChopped("".join(v)) if t is ActType.TALK  else strDuplicatedChopped("。".join(v) + "。")
    for act in scene.actions:
        if act.act_type is ActType.TAG:
            if act.tag_type is TagType.BR:
                res.append(DataPack("tag", "\n"))
            elif act.tag_type is TagType.SYMBOL:
                res.append(DataPack("tag", f"\n　　　　{act.note}\n"))
            elif act.tag_type is TagType.TITLE:
                res.append("tag", f"# {act.note}")
            else:
                continue
        if not inAct:
            act_type = act.act_type
            inAct = True
        for shot in [v for v in act.acts if isinstance(v, Shot)]:
            tmp.append(_descFromShot(shot))
            if shot.isTerm:
                res.append(DataPack(_actTypeStr(act_type), _descCombined(act_type, tmp)))
                tmp = []
                inAct = False
    if tmp:
        res.append(DataPack(_actTypeStr(act_type), _descCombined(act_type, tmp)))
    return (titlePacked(scene),) + tuple(res)

''' to description with rubi
'''
def _toDescsFromWithRubi(src: Tuple[DataPack, ...], rubis: dict) -> Tuple[DataPack, ...]:
    tmp = []
    discards = []
    def _check_exclude(val, words):
        for w in assertion.isTuple(words):
            if w and w in val:
                return True
        return False
    for v in src:
        assertion.isInstance(v, DataPack)
        if "title" in v.head:
            tmp.append(v)
        else:
            desc = v.body
            for k,w in rubis.items():
                if k in discards:
                    continue
                elif k in desc and not f"｜{k}" in desc and not f"{k}《" in desc:
                    if w.exclusions and _check_exclude(desc, w.exclusions):
                        continue
                    desc = desc.replace(k, w.rubi, 1)
                    if not w.isAlways:
                        discards.append(k)
            tmp.append(DataPack(v.head, desc))
    return tuple(tmp)

''' to outline (comment)
'''
def _toOutlinesFrom(story: Story) -> Tuple[DataPack, ...]:
    return (titlePacked(story),) + tuple(
            chain.from_iterable(_toOutlinesFromChapter(v) for v in story.chapters))

def _toOutlinesFromChapter(chapter: Chapter) -> Tuple[DataPack, ...]:
    return (titlePacked(chapter),) + tuple(
            chain.from_iterable(_toOutlinesFromEpisode(v) for v in chapter.episodes))

def _toOutlinesFromEpisode(episode: Episode) -> Tuple[DataPack, ...]:
    return (titlePacked(episode),) + tuple(
            chain.from_iterable(_toOutlinesFromScene(v) for v in episode.scenes))

def _toOutlinesFromScene(scene: Scene) -> Tuple[DataPack, ...]:
    tmp = []
    for act in scene.actions:
        if act.act_type is ActType.TAG and act.tag_type is TagType.COMMENT:
            tmp.append(act.note)
    return (titlePacked(scene),
            DataPack("outline", "/".join(tmp)))


## utility
def _descFromShot(shot: Shot) -> str:
    return "".join(shot.infos)

