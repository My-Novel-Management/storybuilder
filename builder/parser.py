# -*- coding: utf-8 -*-
"""Define tool for parser
"""
## public libs
from itertools import chain
from typing import Any, Tuple
## local libs
from utils import assertion
from utils.util_str import strDuplicatedChopped, dictCombined, containsWordsIn
from utils.util_str import strJoinIf
from builder.utility import hasThen
## local files
from builder import ActType, DataType, TagType, MetaType
from builder import ConteData
from builder.action import Action
from builder.chapter import Chapter
from builder.conjuction import Then
from builder.day import Day
from builder.episode import Episode
from builder.extractor import Extractor
from builder.item import Item
from builder.metadata import MetaData
from builder.person import Person
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word


## define types
StoryLike = (Story, Chapter, Episode, Scene)
DescriptionLike = (DataType.DESCRIPTION, DataType.DIALOGUE, DataType.MONOLOGUE,
                    DataType.NARRATION, DataType.VOICE)
DialogueLike = (ActType.TALK, ActType.THINK, ActType.EXPLAIN, ActType.VOICE)
ObjectLike = (Person, Stage, Day, Time, Item, Word)


## define class
class Parser(object):
    """The tool class for parser
    """
    ## methods
    @classmethod
    def toContes(cls, src: StoryLike) -> Tuple[DataType, Any]:
        # TODO: その他の情報とかを乗せるかどうか
        #       例えばカメラ等の諸情報や、舞台設備など
        if isinstance(src, Scene):
            tmp = []
            tmp.append((DataType.SCENE_SETTING,
                {"stage":src.stage.name,
                    "camera":src.camera.name,
                    "day":src.day.data,
                    "week":src.day.data.weekday(),
                    "time":src.time.name,
                    }))
            persons = set(Extractor.subjectsFrom(src) + Extractor.personsFrom(src))
            items = set(Extractor.itemsFrom(src))
            if src.stage.textures:
                tmp.append((DataType.STAGE_SETTING, dictCombined({"name":src.stage.name},src.stage.textures)))
            if src.camera.textures:
                tmp.append((DataType.PERSON_SETTING, dictCombined({"name":src.camera.name}, src.camera.textures)))
                persons = persons | set([src.camera,])
            ## NOTE: 人物情報
            ## TODO: 文章の人名からも取得できるようにする
            for v in persons:
                if v.textures:
                    tmp.append((DataType.PERSON_SETTING, dictCombined({"name":v.name}, v.textures)))
            ## NOTE: 小道具情報
            ## TODO: 文章中からも取得できるようにする
            for v in items:
                if v.textures:
                    tmp.append((DataType.SCENE_OBJECT, dictCombined({"name":v.name}, v.textures)))
            for ac in src.data:
                if ActType.TAG is ac.act_type:
                    continue
                elif ActType.META is ac.act_type:
                    continue
                else:
                    tmp.append((DataType.ACTION,
                        ConteData(ac.act_type,
                            cls.conteDialogueOf(ac),
                            ac.subject.name,
                            cls.conteObjectsOf(ac),
                            cls.conteContentOf(ac),
                            ac.itemCount,
                            ac.note,
                            )))
            return (cls.titleOf(src),) + tuple(tmp)
        else:
            return (cls.titleOf(src),) + tuple(chain.from_iterable(
                                    [cls.toContes(v) for v in src.data]))

    @classmethod
    def toDescriptions(cls, src: StoryLike) -> Tuple[DataType, Any]:
        def _conv(descs, desc_type, ac, inPara):
            return (desc_type if inPara else cls.descTypeOf(ac),
                    strDuplicatedChopped("。".join(descs)))
        if isinstance(src, Scene):
            tmp = []
            descs = []
            desc_type = DataType.DESCRIPTION
            inPara = False
            last_action = None
            for ac in src.data:
                last_action = ac
                if ActType.META is ac.act_type:
                    continue
                if not ac.tag_type is TagType.NONE:
                    tmp.append(cls.tagOf(ac))
                elif not Extractor.stringsFrom(ac):
                    continue
                else:
                    descs.append(cls.descFrom(ac))
                    if hasThen(ac):
                        if not inPara:
                            inPara = True
                            desc_type = cls.descTypeOf(ac)
                    else:
                        tmp.append(_conv(descs, desc_type, ac, inPara))
                        descs = []
                        inPara = False
            if descs:
                tmp.append(_conv(descs, desc_type, last_action, inPara))
            return (cls.titleOf(src),) + tuple(tmp)
        else:
            return (cls.titleOf(src),) + tuple(chain.from_iterable(
                                [cls.toDescriptions(v) for v in src.data]))

    @classmethod
    def toDescriptionsWithRubi(cls, src: StoryLike, rubis: dict) -> Tuple[DataType, Any]:
        descs = cls.toDescriptions(src)
        tmp = []
        discards = []
        def _check_exclude(val, words):
            for w in assertion.isTuple(words):
                if w and w in val:
                    return True
            return False
        for v in descs:
            if not v[0] in DescriptionLike:
                tmp.append(v)
            else:
                dsc = v[1]
                for k,w in rubis.items():
                    if k in discards:
                        continue
                    elif k in dsc and not f"｜{k}" in dsc and not f"{k}《" in dsc:
                        if w.exclusions and _check_exclude(dsc, w.exclusions):
                            continue
                        dsc = dsc.replace(k, w.data, 1)
                        if not w.isAlways:
                            discards.append(k)
                tmp.append((v[0], dsc))
        return tuple(tmp)

    @classmethod
    def toOutlines(cls, src: StoryLike) -> Tuple[DataType, Any]:
        if isinstance(src, Scene):
            tmp = []
            for ac in src.data:
                if ac.tag_type is TagType.COMMENT:
                    tmp.append((DataType.DATA_STR, ac.note))
            return (cls.titleOf(src), (DataType.DATA_STR, src.note) if src.note else ()) + tuple(tmp)
        else:
            return (cls.titleOf(src), (DataType.DATA_STR, src.note) if src.note else ()) + tuple(chain.from_iterable(
                [cls.toOutlines(v) for v in src.data]))

    @classmethod
    def toLayerInfo(cls, src: StoryLike, words: (str, list, tuple)) -> Tuple[DataType, Action]:
        if isinstance(src, Scene):
            tmp = []
            for ac in src.data:
                if not ac.tag_type is TagType.NONE:
                    continue
                else:
                    descs = strJoinIf(Extractor.stringsFrom(ac), "/")
                    objs = strJoinIf([v.name for v in Extractor.objectsFrom(ac)], "/")
                    if containsWordsIn(descs, words):
                        tmp.append((DataType.DATA_STR, f"「{descs}」" if ac.act_type is ActType.TALK else descs))
                    if containsWordsIn(objs, words):
                        tmp.append((DataType.DATA_STR, objs))
            return (cls.titleOf(src),) + tuple(tmp)
        else:
            return (cls.titleOf(src),) + tuple(chain.from_iterable(
                [cls.toLayerInfo(v, words) for v in src.data]))

    ## methods (for parts)
    @classmethod
    def conteContentOf(cls, action: Action) -> str:
        meta = "/".join([v.note for v in Extractor.metadataFrom(action) if v.data is MetaType.INFO])
        if action.act_type in DialogueLike:
            return meta
        else:
            if meta:
                return meta
            else:
                return strDuplicatedChopped("。".join(Extractor.stringsFrom(action)))

    @classmethod
    def conteDialogueOf(cls, action: Action) -> str:
        if action.act_type in DialogueLike:
            return strDuplicatedChopped("。".join(Extractor.stringsFrom(action)))
        else:
            return ""

    @classmethod
    def conteObjectsOf(cls, action: Action) -> tuple:
        return tuple([v for v in Extractor.directionsFrom(action) if isinstance(v, ObjectLike)])

    @classmethod
    def descFrom(cls, action: Action) -> str:
        tmp = "。".join(Extractor.stringsFrom(action))
        if not action.act_type is ActType.TALK:
            tmp += "。"
        return strDuplicatedChopped(tmp)

    @classmethod
    def descTypeOf(cls, action: Action) -> DataType:
        if action.act_type is ActType.TALK:
            return DataType.DIALOGUE
        elif action.act_type is ActType.THINK:
            return DataType.MONOLOGUE
        elif action.act_type is ActType.EXPLAIN:
            return DataType.NARRATION
        elif action.act_type is ActType.VOICE:
            return DataType.VOICE
        else:
            return DataType.DESCRIPTION

    @classmethod
    def tagOf(cls, action: Action) -> Tuple[DataType, str]:
        if action.tag_type is TagType.BR:
            return (DataType.TAG, "\n")
        elif action.tag_type is TagType.COMMENT:
            return (DataType.TAG, action.note)
        elif action.tag_type is TagType.OUTLINE:
            return (DataType.TAG, action.note)
        elif action.tag_type is TagType.HR:
            return (DataType.TAG, "--------" * 8)
        elif action.tag_type is TagType.SYMBOL:
            return (DataType.TAG, action.note)
        elif action.tag_type is TagType.TITLE:
            return (DataType.TITLE, action.note)
        else:
            return (DataType.NONE, "")

    @classmethod
    def titleOf(cls, src: StoryLike) -> Tuple[DataType, str]:
        if isinstance(src, Story):
            return (DataType.STORY_TITLE, src.title)
        elif isinstance(src, Chapter):
            return (DataType.CHAPTER_TITLE, src.title)
        elif isinstance(src, Episode):
            return (DataType.EPISODE_TITLE, src.title)
        else:
            return (DataType.SCENE_TITLE, assertion.isInstance(src, Scene).title)
