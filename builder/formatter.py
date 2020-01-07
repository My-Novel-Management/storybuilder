# -*- coding: utf-8 -*-
"""Define tool for format
"""
## public libs
## local libs
from utils import assertion
from utils.util_str import strEllipsis
## local files
from builder import DataType, ConteData
from builder import ActType, TagType
from builder.analyzer import Analyzer
from builder.extractor import Extractor


## define types
TitleLike = (DataType.STORY_TITLE, DataType.CHAPTER_TITLE, DataType.EPISODE_TITLE,
        DataType.SCENE_TITLE)


## define class
class Formatter(object):
    """The tool class for format
    """

    ## methods
    @classmethod
    def toConte(cls, title: str, src: list, analyzer: Analyzer) -> list:
        tmp = []
        discards = [] # for texture
        def _weekday(v):
            return ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")[v]
        def _conv(act_type, dialogue, subject, objects, content, count, note):
            atype = act_type.name.upper()[0:2]
            sub_obj = f"{subject}{objects}"
            dial = strEllipsis(dialogue, 24)
            sub = strEllipsis(sub_obj + f"×{count:2d}", 32) if count else strEllipsis(sub_obj, 32)
            sub = f"{sub:\u3000<33}" if count else f"{sub:\u3000<32}"
            cont = strEllipsis(content, 24)
            return f"{atype}|{dial:\u3000<24}|{sub:\u3000<32}|{cont:\u3000<24}|{note}"
        def _objs(objects):
            return "".join([f"［{v.name}］" for v in objects])
        def _texture(data: dict):
            tmp = []
            for k,v in data.items():
                if "name" == k:
                    tmp.append(f"[{v}]:")
                else:
                    tmp.append(f"{k}:{v}")
            return "/".join(tmp)
        for v in cls.srcConvertedTitleWithNum(src):
            data = v[1]
            if v[0] in TitleLike:
                tmp.append(v[1])
            elif DataType.TAG is v[0]:
                ## TODO
                continue
            ## settings
            elif DataType.SCENE_SETTING is v[0]:
                tmp.append(f"○{data['stage']}（{data['time']}） - {data['day']}({_weekday(data['week'])}) - ＜{data['camera']}＞")
            elif DataType.PERSON_SETTING is v[0] and not data['name'] in discards:
                tmp.append(_texture(data))
                discards.append(data['name'])
            elif DataType.STAGE_SETTING is v[0] and not data['name'] in discards:
                tmp.append(_texture(data))
                discards.append(data['name'])
            elif DataType.SCENE_OBJECT is v[0] and not data['name'] in discards:
                tmp.append(_texture(data))
                discards.append(data['name'])
            ## word like
            elif isinstance(data, ConteData):
                if ActType.TALK is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, data.dialogue, name,
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.THINK is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"（{data.dialogue}", name,
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.EXPLAIN is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"＃{data.dialogue}", name,
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.VOICE is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"『{data.dialogue}", name,
                        _objs(data.objects), data.content, data.count, data.note))
                ## effects
                elif ActType.HEAR is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"♪{data.dialogue}", name,
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.LOOK is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, data.dialogue, name,
                        _objs(data.objects), data.content, data.count, data.note))
                ## control
                elif ActType.BE is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"［{data.subject}］",
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.DESTROY is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"〜{data.subject}",
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.HAVE is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, data.dialogue, name,
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.DISCARD is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"{data.subject}〜",
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.COME is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"→［{data.subject}］",
                        _objs(data.objects), data.content, data.count, data.note))
                elif ActType.GO is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"←〜{data.subject}",
                        _objs(data.objects), data.content, data.count, data.note))
                ## others
                else:
                    name = strEllipsis(data.subject, 3, "")
                    acts = analyzer.verbs(data.content)
                    subject = f"{name}" + "".join([f"〈{v}〉" for v in acts])
                    tmp.append(_conv(data.type, data.dialogue, subject,
                        "".join([f"［{v}］" for v in data.objects]), data.content, data.count, data.note))
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toDescription(cls, title: str, src: list, spacing: list) -> list:
        ## NOTE:
        ##  spacing (line-line, line-dialogue, dialogue-line, dialogue-dialogue)
        tmp = []
        ch_num, ep_num, sc_num = 1, 1, 1
        inDialogue = False
        ll_sp = "\n" * spacing[0]
        ld_sp = "\n" * spacing[1]
        dl_sp = "\n" * spacing[2]
        dd_sp = "\n" * spacing[3]
        for v in cls.srcConvertedTitleWithNum(src):
            if v[0] in TitleLike:
                tmp.append(v[1])
            elif v[0] in (DataType.DIALOGUE, DataType.VOICE):
                base = f"「{v[1]}」" if DataType.DIALOGUE is v[0] else f"『{v[1]}』"
                if inDialogue: # D-D
                    tmp.append(f"{dd_sp}{base}")
                else: # L-D
                    tmp.append(f"{ld_sp}{base}")
                    inDialogue = True
            else:
                if inDialogue: # D-L
                    tmp.append(f"{dl_sp}　{v[1]}")
                else: # L-L
                    tmp.append(f"{ll_sp}　{v[1]}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toGeneralInfo(cls, title: str, src: list, isActtype: bool=True) -> list:
        tmp = [f"# {title}\n"] + cls.toCharactersInfo(src)
        acttypes = cls.toActionTypeInfo(src)
        if isActtype:
            return tmp + ["\n"] + acttypes
        else:
            return tmp

    @classmethod
    def toGeneralInfoEachScene(cls, title: str, src: list) -> list:
        tmp = cls.toCharactersInfo(src, False)
        acttypes = cls.toActionTypeInfo(src)
        return [f"# {title}\n"] + tmp + ["--------" * 8] + acttypes

    @classmethod
    def toCharactersInfo(cls, src: list, isSceneCount: bool=True) -> list:
        tmp = []
        total, manupaper, rows, columns = 0, 0, 0, 0
        chapters, episodes, scenes, actions = 0, 0, 0, 0
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n## {data[1]}\n")
            elif DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    if "total" == k:
                        total = v
                    elif "manupaper" == k:
                        manupaper = v
                    elif "rows" == k:
                        rows = v
                    elif "columns" == k:
                        columns == v
                    elif "chapters" == k:
                        chapters == v
                    elif "episodes" == k:
                        episodes = v
                    elif "scenes" == k:
                        scenes = v
                    elif "actions" == k:
                        actions = v
                papers = manupaper / rows if rows else 0
                tmp.append(f"> Total: {total}c / [{papers:.2f}p ({manupaper:.2f}ls)]")
                if isSceneCount:
                    tmp.append(f"> Chapters: {chapters} / Episodes: {episodes} / Scenes: {scenes} / Actions: {actions}")
                total, manupaper, rows, columns = 0, 0, 0, 0
                chapters, episodes, scenes, actions = 0, 0, 0, 0
        return tmp

    @classmethod
    def toActionTypeInfo(cls, src: list) -> list:
        tmp = []
        act_total = 0
        acttypes = []
        def _percent(v, total):
            return v / total * 100 if total else 0
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n## {data[1]}\n")
            elif DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    if "acttype_total" == k:
                        act_total = v
                    elif "acttype" in k:
                        acttypes.append(v)
                talk_percent = acttypes[cls.getTalkIndex()] / sum(acttypes) * 100 if act_total else 0
                tmp.append(f"## Action info: {act_total} / Dialogues: {talk_percent:.2f}%")
                tmp.append("|".join(sorted([f"{strEllipsis(v.name,3,''):<6}" for v in ActType])))
                tmp.append("|".join(sorted([f"{v:>6}" for v in [f"{_percent(v, act_total):.2f}%" for t,v in zip(ActType, acttypes)]])))
                act_total = 0
                acttypes = []
        return tmp

    @classmethod
    def toKanjiInfo(cls, title: str, src: list) -> list:
        tmp = []
        total, kanji = 0, 0
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n## in {data[1]}\n")
            if DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    if "total" in k:
                        total = v
                    elif "kanji" in k:
                        kanji = v
                percent = kanji / total * 100 if total else 0
                tmp.append(f"* Kanji: {percent:.2f}% - {kanji}c / {total}c")
        return [f"# {title}\n",] + tmp

    @classmethod
    def toOutline(cls, title: str, src: list) -> list:
        tmp = []
        for data in cls.srcConvertedTitleWithNum(src):
            if data[0] in TitleLike:
                tmp.append(data[1])
            elif DataType.DATA_STR is data[0]:
                tmp.append(f"\t{data[1]}")
        return [f"# {title}\n",] + tmp

    @classmethod
    def toLayerInfo(cls, title: str, src: list) -> list:
        tmp = []
        total, dialogues = 0, 0 
        for data in cls.srcConvertedTitleAsLayer(src):
            if data[0] in TitleLike:
                tmp.append(data[1])
            elif DataType.HEAD is data[0]:
                tmp.append(f"\n## {data[1]}\n")
            elif DataType.DATA_STR is data[0]:
                base = f"- {data[1]}"
                if data[1].startswith('「'):
                    base = f"* {data[1]}"
                    dialogues += 1
                tmp.append(f"    {base}")
                total += 1
        return [f"# {title}\n", f"## Total: {total} / Dialogues: {dialogues}\n",
                ] + tmp

    @classmethod
    def toListInfo(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    tmp.append(f"- {k:<24} | {v.name:\u3000<24} | {v.note}")
        return [f"# {title}\n",] + tmp

    @classmethod
    def toListDayTimes(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    tmp.append(f"- {k:<24} | {v.name:\u3000<24} | {v.data}")
        return [f"# {title}\n",] + tmp

    @classmethod
    def toListPersons(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    full = v.fullname.replace(',','')
                    tmp.append(f"- {k:<24} | {v.name:\u3000<10} | {full:\u3000<12} | {v.age}歳 | {v.sex:<6} | {v.job:\u3000<10} | {v.note}")
        return [f"# {title}\n",] + tmp

    @classmethod
    def toWordClassInfo(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n## {data[1]}\n")
            elif DataType.DATA_STR is data[0]:
                tmp.append(f"- {data[1]}")
        return [f"# {title}\n",
                ] + tmp

    ## methods (for titles)
    @classmethod
    def srcConvertedTitleWithNum(cls, src: list) -> list:
        tmp = []
        ch, ep, sc = 1, 1, 1
        for v in src:
            if not v:
                continue
            if DataType.STORY_TITLE is v[0]:
                tmp.append((v[0], f"# {v[1]}\n"))
            elif DataType.CHAPTER_TITLE is v[0]:
                tmp.append((v[0], f"\n## Ch-{ch}: {v[1]}\n"))
                ch += 1
            elif DataType.EPISODE_TITLE is v[0]:
                tmp.append((v[0], f"\n### Ep-{ep}: {v[1]}\n"))
                ep += 1
            elif DataType.SCENE_TITLE is v[0]:
                tmp.append((v[0], f"\n** Sc-{sc}: {v[1]} **\n"))
                sc += 1
            else:
                tmp.append(v)
        return tmp

    @classmethod
    def srcConvertedTitleAsLayer(cls, src: list) -> list:
        tmp = []
        ch, ep, sc = 1, 1, 1
        for v in src:
            if not v:
                continue
            if DataType.STORY_TITLE is v[0]:
                ch, ep, sc = 1, 1, 1
                continue
            elif DataType.CHAPTER_TITLE is v[0]:
                tmp.append((v[0], f"[in Ch-{ch}]: {v[1]}"))
                ch += 1
            elif DataType.EPISODE_TITLE is v[0]:
                tmp.append((v[0], f"[in Ep-{ep}]: {v[1]}"))
                ep += 1
            elif DataType.SCENE_TITLE is v[0]:
                tmp.append((v[0], f"[in Sc-{sc}]: {v[1]}"))
                sc += 1
            else:
                tmp.append(v)
        return tmp

    @classmethod
    def getTalkIndex(cls) -> int:
        idx = 0
        for v in ActType:
            if v is ActType.TALK:
                return idx
            else:
                idx += 1
        return idx
