# -*- coding: utf-8 -*-
"""Define tool for counting
"""
## public libs
from itertools import chain
## local libs
from utils import assertion
from utils.util_math import intCeiled
from utils.util_str import kanjiOf, strDuplicatedChopped
from builder.utility import hasThen
## local files
from builder import ActType, MetaType
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.extractor import Extractor
from builder.scene import Scene
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


## define class
class Counter(object):
    """The tool for counting something.
    """
    ## methods (basic)
    @classmethod
    def actions(cls, src: StoryLike) -> int:
        return len(Extractor.actionsFrom(src))

    @classmethod
    def actType(cls, src: StoryLike, act_type: ActType) -> int:
        return len([v for v in Extractor.actionsFrom(src) if v.act_type is act_type])

    @classmethod
    def chapters(cls, src: StoryLike) -> int:
        if isinstance(src, (Story, Chapter)):
            return len(Extractor.chaptersFrom(src))
        else:
            return 0

    @classmethod
    def episodes(cls, src: StoryLike) -> int:
        if isinstance(src, (Story, Chapter, Episode)):
            return len(Extractor.episodesFrom(src))
        else:
            return 0

    @classmethod
    def scenes(cls, src: StoryLike) -> int:
        return len(Extractor.scenesFrom(src))

    ## methods (characters)
    @classmethod
    def descriptions(cls, src: StoryLike) -> int:
        tmp = Extractor.stringsFrom(src)
        chars = strDuplicatedChopped("。".join(tmp))
        return len(tmp) * 2 + len(chars)

    @classmethod
    def kanjis(cls, src: StoryLike) -> int:
        return sum(len(kanjiOf(v)) for v in Extractor.stringsFrom(src))

    @classmethod
    def metainfos(cls, src: StoryLike) -> int:
        tmp = [v.note for v in Extractor.metadataFrom(src) if v.data is MetaType.INFO]
        return sum(len(v) for v in tmp)

    @classmethod
    def noteChars(cls, src: StoryLike) -> int:
        if isinstance(src, (Scene, Action)):
            return 0
        else:
            return sum(cls.noteChars(v) for v in src.data) + len(src.note)

    ## methods (manupapers)
    @classmethod
    def manupaperRows(cls, src: StoryLike, column: int) -> int:
        def _conv(v, c):
            return intCeiled(v + 2, c)
        if isinstance(src, Scene):
            res = []
            tmp = 0
            for ac in src.data:
                tmp += sum([len(v) for v in Extractor.stringsFrom(ac)])
                if not hasThen(ac):
                    res.append(_conv(tmp, column))
                    tmp = 0
            if tmp:
                res.append(_conv(tmp, column))
            res.append(len([v for v in Extractor.brTagsFrom(src)]))
            res.append(sum([3 for v in Extractor.symbolesFrom(src)]))
            return sum(res)
        else:
            return sum(cls.manupaperRows(v, column) for v in src.data)

