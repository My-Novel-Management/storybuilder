# -*- coding: utf-8 -*-
"""Define tool for parser
"""
## public libs
import datetime
from dateutil.relativedelta import relativedelta
from itertools import chain
from typing import Any, Tuple, List
## local libs
from utils import assertion
from utils.util_str import strDuplicatedChopped, dictCombined, containsWordsIn, strReplacedTagByDict
from utils.util_str import strJoinIf
from builder.utility import hasThen
## local files
from builder import ActType, DataType, TagType, MetaType
from builder import ConteData
from builder import History
from builder.action import Action
from builder.analyzer import Analyzer
from builder.area import Area
from builder.chapter import Chapter
from builder.converter import Converter
from builder.conjuction import Then
from builder.counter import Counter
from builder.day import Day
from builder.episode import Episode
from builder.extractor import Extractor
from builder.item import Item
from builder.lifenote import LifeNote
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
    def toContes(cls, src: StoryLike, is_comment: bool=False) -> Tuple[DataType, Any]:
        # TODO: その他の情報とかを乗せるかどうか
        #       例えばカメラ等の諸情報や、舞台設備など
        def _hasMetaBlock(ac: Action, isEnd: bool):
            tmp = Extractor.metadataFrom(ac)
            for v in tmp:
                if isEnd and v.data is MetaType.BLOCK_END:
                    return True
                elif v.data is MetaType.BLOCK_START:
                    return True
            else:
                return False
        def _hasMetaEvent(ac: Action):
            tmp = Extractor.metadataFrom(ac)
            for v in tmp:
                if v.data in (MetaType.EVENT_END, MetaType.EVENT_POINT, MetaType.EVENT_START):
                    return v.data
            else:
                return None
        if isinstance(src, Scene):
            tmp = []
            scene_sbjs = []
            scene_objs = []
            discards = []
            tmp.append((DataType.SCENE_SETTING,
                {
                    "area":src.area.name,
                    "stage":src.stage.name,
                    "camera":src.camera.name,
                    "day":src.day.data,
                    "week":src.day.data.weekday(),
                    "time":src.time.name,
                    }))
            persons = set(Extractor.subjectsFrom(src) + Extractor.personsFrom(src))
            items = set(Extractor.itemsFrom(src))
            if src.stage.texture:
                name, tex = src.stage.name, src.stage.texture
                if not name + tex in discards:
                    tmp.append((DataType.STAGE_SETTING, {"name":name,"texture":tex}))
                    discards.append(name + tex)
            if src.camera.texture:
                name, tex = src.camera.name, src.camera.texture
                if not name + tex in discards:
                    tmp.append((DataType.PERSON_SETTING, {"name":name, "texture":tex}))
                    discards.append(name + tex)
                persons = persons | set([src.camera,])
            ## NOTE: 人物情報
            ## TODO: 文章の人名からも取得できるようにする
            for v in persons:
                if v.texture:
                    name, tex = v.name, v.texture
                    if not name + tex in discards:
                        tmp.append((DataType.PERSON_SETTING, {"name":name, "texture":tex}))
                        discards.append(name + tex)
            ## NOTE: 小道具情報
            ## TODO: 文章中からも取得できるようにする
            for v in items:
                if v.texture:
                    name, tex = v.name, v.texture
                    if not name + tex in discards:
                        tmp.append((DataType.SCENE_OBJECT, {"name":name, "texture":tex}))
                        discards.append(name + tex)
            ## texture
            for ac in src.data:
                if ActType.WEAR is ac.act_type:
                    name, tex = ac.subject.name, cls.conteContentOf(ac)
                    if not name + tex in discards:
                        tmp.append((DataType.SCENE_OBJECT, {"name":name, "texture":tex}))
                        discards.append(name + tex)
            for ac in src.data:
                if ActType.TAG is ac.act_type:
                    if ac.tag_type in (TagType.BR, TagType.SYMBOL):
                        continue
                    elif TagType.COMMENT is ac.tag_type and not is_comment:
                        continue
                    else:
                        tmp.append(cls.tagOf(ac))
                elif ActType.META is ac.act_type:
                    if _hasMetaBlock(ac, False):
                        title = [v for v in Extractor.metadataFrom(ac) if v.data is MetaType.BLOCK_START][0].name
                        tmp.append((DataType.META, f"blockstart:{title}"))
                    elif _hasMetaBlock(ac, True):
                        title = [v for v in Extractor.metadataFrom(ac) if v.data is MetaType.BLOCK_END][0].name
                        tmp.append((DataType.META, f"blockend:{title}"))
                    elif _hasMetaEvent(ac):
                        meta = _hasMetaEvent(ac)
                        title = [v for v in Extractor.metadataFrom(ac) if v.data is meta][0].name
                        note = [v for v in Extractor.metadataFrom(ac) if v.data is meta][0].note
                        if MetaType.EVENT_END is meta:
                            tmp.append((DataType.META, f"eventend:{title}:{note}"))
                        elif MetaType.EVENT_START is meta:
                            tmp.append((DataType.META, f"eventstart:{title}:{note}"))
                        else:
                            tmp.append((DataType.META, f"event:{title}:{note}"))
                    else:
                        continue
                else:
                    scene_sbjs += Extractor.subjectsFrom(ac)
                    scene_objs += Extractor.objectsFrom(ac)
                    tmp.append((DataType.ACTION,
                        ConteData(ac.act_type,
                            cls.conteDialogueOf(ac),
                            ac.subject.name,
                            cls.conteObjectsOf(ac),
                            cls.conteContentOf(ac),
                            ac.itemCount,
                            ac.note,
                            )))
            tmp.append((DataType.DATA_LIST, list(set([v.name for v in scene_sbjs]))))
            tmp.append((DataType.DATA_LIST, list(set([v.name for v in scene_objs]))))
            char_count = Counter.metainfos(src) + Counter.descriptions(src)
            return ((DataType.SCENE_TITLE, f"{src.title} [{char_count}]c"),) + tuple(tmp)
        else:
            return (cls.titleOf(src),) + tuple(chain.from_iterable(
                                    [cls.toContes(v, is_comment) for v in src.data]))

    @classmethod
    def toDescriptions(cls, src: StoryLike, is_comment: bool=False) -> Tuple[DataType, Any]:
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
                    if ac.tag_type is TagType.COMMENT and not is_comment:
                            continue
                    else:
                        tmp.append(cls.tagOf(ac))
                elif not Extractor.stringsFrom(ac):
                    continue
                elif ActType.WEAR is ac.act_type:
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
            char_count = Counter.descriptions(src)
            return ((DataType.SCENE_TITLE, f"{src.title} [{char_count}]c"),) + tuple(tmp)
        elif isinstance(src, Episode):
            char_count = Counter.descriptions(src)
            return ((DataType.EPISODE_TITLE, f"{src.title} [{char_count}]c"),) + tuple(
                    chain.from_iterable([cls.toDescriptions(v, is_comment) for v in src.data])
                    )
        else:
            return (cls.titleOf(src),) + tuple(chain.from_iterable(
                                [cls.toDescriptions(v, is_comment) for v in src.data]))

    @classmethod
    def toDescriptionsWithRubi(cls, src: StoryLike, rubis: dict, is_comment: bool=False) -> Tuple[DataType, Any]:
        descs = cls.toDescriptions(src, is_comment)
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
    def toHistory(cls, subject: Person, basedate: datetime.date, src: List[History]) -> list:
        tmp = []
        birth = basedate - relativedelta(years=subject.age)
        tmp.append(History(birth + relativedelta(month=subject.birth[0], day=subject.birth[1]),
            "0:誕生日", ""))
        ## reorder date
        for hi in src:
            day = birth
            if isinstance(hi.date, int):
                day = birth + relativedelta(years=hi.date)
            elif isinstance(hi.date, str) and ":" in hi.date:
                years = hi.date.split(':')
                if len(years) == 2:
                    day = birth + relativedelta(years=int(years[0]), months=int(years[1]))
                else:
                    day = birth + relativedelta(years=int(years[0]), months=int(years[1]), days=int(years[2]))
            elif isinstance(hi.date, str) and "-" in hi.date:
                day = datetime.date.fromisoformat(hi.date)
            else:
                day = birth
            age = (day - birth).days / 365
            tmp.append(History(day, f"{age}:{hi.content}", hi.note))
        return sorted(tmp, key=lambda h: h[0])

    @classmethod
    def toInfoVolumes(cls, src: Story, analyzer: Analyzer) -> list:
        tmp = []
        discards = []
        for ch in src.data:
            tmp.append(cls.titleOf(ch))
            for ep in ch.data:
                tmp.append(cls.titleOf(ep))
                for sc in ep.data:
                    tmp.append(cls.titleOf(sc))
                    vols = 0
                    fvols = 0
                    for ac in sc.data:
                        dires = Extractor.stringsFrom(ac)
                        azd = analyzer.collectionsFrom(dires)
                        for wcls,lst in azd.items():
                            for v in lst:
                                vols += wcls.convVolume()
                                if not v in discards:
                                    discards.append(v)
                                    fvols += wcls.convVolume()
                    tmp.append((DataType.DATA_STR, f"{fvols}/{vols}"))
        return tmp

    @classmethod
    def toLifeNote(cls, src: LifeNote, tags: dict, prefix: str) -> Tuple[DataType, Any]:
        tmp = []
        notes = []
        current = src.subject
        for ac in src.data:
            conv_act, current = Converter.actionReplacedPronoun(ac, current)
            conv_act = Converter.actionReplacedTags(conv_act, tags, prefix, current)
            notes.append(conv_act)
        sc = Scene(strReplacedTagByDict(src.title, tags, prefix), *notes)
        return cls.toDescriptions(sc)

    @classmethod
    def toOutlines(cls, src: StoryLike) -> Tuple[DataType, Any]:
        if isinstance(src, Scene):
            tmp = []
            for ac in src.data:
                if ac.tag_type is TagType.COMMENT:
                    tmp.append((DataType.DATA_STR, ac.note))
            return (cls.titleOf(src), (DataType.DATA_STR, src.note) if src.note else (DataType.NONE, "")) + tuple(tmp)
        else:
            return (cls.titleOf(src), (DataType.DATA_STR, src.note) if src.note else (DataType.NONE,"")) + tuple(chain.from_iterable(
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
        if not action.act_type in (ActType.TALK, ActType.VOICE):
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
            return (DataType.TAG, f"<!--{action.note}-->")
        elif action.tag_type is TagType.OUTLINE:
            return (DataType.TAG, action.note)
        elif action.tag_type is TagType.HR:
            return (DataType.TAG, "--------" * 8)
        elif action.tag_type is TagType.SYMBOL:
            return (DataType.TAG, f"\n{action.note}\n")
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
