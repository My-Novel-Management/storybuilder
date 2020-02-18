# -*- coding: utf-8 -*-
"""Define tool for format
"""
## public libs
import datetime
## local libs
from utils import assertion
from utils.util_str import strEllipsis ,hanToZen
## local files
from builder import __WALK_STAGE__, __DRIVE_STAGE__
from builder import DataType, ConteData
from builder import ActType, TagType
from builder.analyzer import Analyzer
from builder.area import Area
from builder.counter import Counter
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
    def toActionEachPerson(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(data[1])
            elif DataType.DATA_DICT is data[0]:
                tmp.append("|".join([f"{k}:{v}" for k,v in data[1].items()]))
        return [f"# {title}\n"] + tmp

    @classmethod
    def toConte(cls, title: str, src: list, analyzer: Analyzer) -> list:
        tmp = []
        class SubMaker(object):
            def __init__(self):
                self.buf = ""
            def getSub(self, cur):
                if cur == self.buf:
                    return "　︙"
                else:
                    self.buf = cur
                    return cur
        def _weekday(v):
            return ("Mon","Tue","Wed","Thu","Fri","Sat","Sun")[v]
        def _getSub(cur, bef, count):
            if cur == bef:
                _ = "︙"
                return f"{_:\u3000<32}"
            else:
                return f"{cur:\u3000<33}" if count else f"{cur:\u3000<32}"
        def _conv(act_type, dialogue, subject, suffix, objects, content, count, note, volume, submaker):
            atype = act_type.emoji() if isinstance(act_type, ActType) else act_type
            subject = submaker.getSub(subject) + suffix
            sub_obj = f"{subject}{objects}"
            dial = strEllipsis(dialogue, 24)
            sub = strEllipsis(sub_obj + f"×{count:2d}", 32) if count else strEllipsis(sub_obj, 32)
            sub = f"{sub:\u3000<33}" if count else f"{sub:\u3000<32}"
            cont = strEllipsis(content, 24)
            vol = Counter.infoVolumeOf(volume, analyzer) if volume else "-"
            return f"{atype}|{dial:\u3000<24}|{sub:\u3000<32}|{cont:\u3000<24}|{vol:>4}|{note}"
        def _convEvent(act_type, dialogue, title, content):
            atype = act_type.emoji() if isinstance(act_type, ActType) else act_type
            dial = strEllipsis(dialogue, 36)
            ttl = strEllipsis(title, 10)
            cont = strEllipsis(f"(:{content})", 38)
            return f"{atype}|{dial:\u3000<36}|[{ttl}]{cont:\u3000<48}|"
        def _objs(objects):
            return "".join([f"［{v.name}］" for v in objects])
        def _texture(data: dict):
            tmp = []
            for k,v in data.items():
                if "name" == k:
                    tmp.append(f"[{v}]:")
                else:
                    tmp.append(f"{v}")
            return "".join(tmp)
        submaker = SubMaker()
        for v in cls.srcConvertedTitleWithNum(src):
            data = v[1]
            if v[0] in TitleLike:
                tmp.append(v[1])
            elif DataType.TAG is v[0]:
                tmp.append(v[1])
            elif DataType.HEAD is v[0]:
                tmp.append(f"\n{v[1]}\n")
            ## settings
            elif DataType.SCENE_SETTING is v[0]:
                tmp.append(f"○{data['stage']}［{data['area']}］（{data['time']}） - {data['day']}({_weekday(data['week'])}) - ＜{data['camera']}＞")
            elif DataType.PERSON_SETTING is v[0]:
                tmp.append(_texture(data))
            elif DataType.STAGE_SETTING is v[0]:
                tmp.append(_texture(data))
            elif DataType.SCENE_OBJECT is v[0]:
                tmp.append(_texture(data))
            ## meta data
            elif DataType.META is v[0]:
                if "blockstart" in v[1]:
                    _, title = v[1].split(":")
                    tmp.append(_convEvent("📼", "ー"*36, title, "開始"))
                elif "blockend" in v[1]:
                    _, title = v[1].split(":")
                    tmp.append(_convEvent("🔚", "ー"*36, title, "終了"))
                elif "eventstart" in v[1]:
                    _, title, note = v[1].split(":")
                    tmp.append(_convEvent("🎬", "※"*36, title, "オープン"))
                elif "eventend" in v[1]:
                    _, title, note = v[1].split(":")
                    tmp.append(_convEvent("🔝", "※"*36, title, "クローズ"))
                elif "event" in v[1]:
                    _, title, note = v[1].split(":")
                    tmp.append(_convEvent("🔑", "※"*36, title, note))
            ## object data
            elif DataType.DATA_LIST is v[0]:
                tmp.append("".join([f"[^{n}]" for n in v[1]]))
            ## word like
            elif isinstance(data, ConteData):
                if ActType.TALK is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"「{data.dialogue}」", f"＞{name}", "",
                        _objs(data.objects), data.content, data.count, data.note, data.dialogue, submaker))
                elif ActType.THINK is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"（{data.dialogue}）", name, "",
                        _objs(data.objects), data.content, data.count, data.note, data.dialogue, submaker))
                elif ActType.EXPLAIN is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"＃{data.dialogue}", name, "",
                        _objs(data.objects), data.content, data.count, data.note, data.dialogue, submaker))
                elif ActType.VOICE is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"『{data.dialogue}』", name, "",
                        _objs(data.objects), data.content, data.count, data.note, data.dialogue, submaker))
                ## effects
                elif ActType.HEAR is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, f"【{data.content}】", name, "",
                        _objs(data.objects), "", data.count, data.note, data.content, submaker))
                elif ActType.LOOK is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, data.dialogue,
                        name, f"｛{data.content}｝",
                        _objs(data.objects), "", data.count, data.note, data.content, submaker))
                elif ActType.WEAR is data.type:
                    continue
                ## control
                elif ActType.BE is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"［{data.subject}］", "",
                        _objs(data.objects), data.content, data.count, data.note,
                        data.subject + data.content, submaker))
                elif ActType.DESTROY is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"〜{data.subject}", "",
                        _objs(data.objects), data.content, data.count, data.note, data.content, submaker))
                elif ActType.HAVE is data.type:
                    name = strEllipsis(data.subject, 3, "")
                    tmp.append(_conv(data.type, data.dialogue, name, "",
                        _objs(data.objects), data.content, data.count, data.note, data.content, submaker))
                elif ActType.DISCARD is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"{data.subject}〜", "",
                        _objs(data.objects), data.content, data.count, data.note, data.content, submaker))
                elif ActType.COME is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"→［{data.subject}］", "",
                        _objs(data.objects), data.content, data.count, data.note, data.content, submaker))
                elif ActType.GO is data.type:
                    tmp.append(_conv(data.type, data.dialogue, f"←〜{data.subject}", "",
                        _objs(data.objects), data.content, data.count, data.note, data.content, submaker))
                ## others
                else:
                    name = strEllipsis(data.subject, 3, "")
                    acts = "／".join([v for v in set(analyzer.verbs(data.content))])
                    tmp.append(_conv(data.type, data.dialogue, name, f"＜{acts}＞",
                        "".join([f"［{v.name}］" for v in data.objects]), data.content, data.count, data.note, data.content, submaker))
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toDescription(cls, title: str, src: list, spacing: list, exceptTitle: bool=False) -> list:
        ## NOTE:
        ##  spacing (line-line, line-dialogue, dialogue-line, dialogue-dialogue)
        tmp = []
        ch_num, ep_num, sc_num = 1, 1, 1
        inDialogue = False
        ll_sp = "\n" * spacing[0]
        ld_sp = "\n" * spacing[1]
        dl_sp = "\n" * spacing[2]
        dd_sp = "\n" * spacing[3]
        for data in cls.srcConvertedTitleWithNum(src):
            if data[0] in TitleLike:
                if not exceptTitle:
                    tmp.append(data[1])
                    inDialogue = False
            elif DataType.TAG is data[0]:
                tmp.append(data[1])
            elif data[0] in (DataType.DIALOGUE, DataType.VOICE):
                base = f"「{data[1]}」" if DataType.DIALOGUE is data[0] else f"『{data[1]}』"
                if inDialogue: # D-D
                    tmp.append(f"{dd_sp}{base}")
                else: # L-D
                    tmp.append(f"{ld_sp}{base}")
                    inDialogue = True
            else:
                if inDialogue: # D-L
                    tmp.append(f"{dl_sp}　{data[1]}")
                    inDialogue = False
                else: # L-L
                    tmp.append(f"{ll_sp}　{data[1]}")
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
        return ["--------" * 8, f"# {title}\n"] + tmp + ["- - - - " * 8] + acttypes

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
                        columns = v
                    elif "chapters" == k:
                        chapters = v
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
    def toHistoryPersons(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n## {data[1]}\n")
            elif DataType.DATA_LIST is data[0]:
                for hi in data[1]:
                    age, cont = hi.content.split(":")
                    _age = f"{float(age):.1f}"
                    tmp.append(f"{hi.date} | {_age:>6} | {cont:\u3000<32} | {hi.note}")
        return [f"# {title}\n"] + tmp

    @classmethod
    def toInfoVolumes(cls, title: str, src: list) -> list:
        tmp = []
        for data in cls.srcConvertedTitleWithNum(src):
            if data[0] in TitleLike:
                tmp.append(data[1])
            elif DataType.DATA_STR is data[0]:
                tmp.append(f"- {data[1]}")
        return [f"# {title}\n"] + tmp

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
    def toLinescaleOfEvents(cls, title: str, src: list) -> list:
        tmp = []
        def _getTitle(v):
            _, sc, title, note = v.split(":")
            return title
        titles = []
        for v in src:
            if v[0] is DataType.DATA_STR:
                title = _getTitle(v[1])
                if not title in titles:
                    titles.append(title)
        head = "|".join(titles)
        def _getNum(title):
            idx = 0
            for v in titles:
                if v == title:
                    return idx
                idx += 1
            return idx
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n{data[1]}\n")
            elif DataType.DATA_STR is data[0]:
                if "start" in data[1]:
                    _, sc, title, note = data[1].split(":")
                    num = _getNum(title)
                    idt = "　" * num
                    sc = strEllipsis(hanToZen(sc), 12)
                    tmp.append(f"{sc:\u3000<12}|{idt}▽[^{title}]")
                elif "end" in data[1]:
                    _, sc, title, note = data[1].split(":")
                    num = _getNum(title)
                    idt = "　" * num
                    sc = strEllipsis(hanToZen(sc), 12)
                    tmp.append(f"{sc:\u3000<12}|{idt}▲")
                elif "point" in data[1]:
                    _, sc, title, note = data[1].split(":")
                    num = _getNum(title)
                    idt = "　" * num
                    sc = strEllipsis(hanToZen(sc), 12)
                    tmp.append(f"{sc:\u3000<12}|{idt}●:{note}")
        return [f"# {title}\n", "## Events\n", head] + tmp

    @classmethod
    def toLinescaleOfPerson(cls, title: str, src: list) -> list:
        tmp = []
        persons = []
        for data in src:
            if DataType.DATA_DICT is data[0]:
                psns = data[1]['persons']
                for p in psns:
                    if not p in persons:
                        persons.append(p)
        def _getList(psns, tops):
            _ = []
            for p in persons:
                if p in psns:
                    for i in range(len(psns)):
                        if p == psns[i]:
                            _.append(tops[i][0].emoji())
                            break
                else:
                    _.append("　")
            return "|".join(_)
        head = "|".join(persons)
        shorthead = "|".join([v[0] for v in persons])
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n{data[1]}\n")
                idt = "　"*10
                tmp.append(f"{idt}|{shorthead}")
            elif DataType.DATA_DICT is data[0]:
                sc = strEllipsis(hanToZen(data[1]['scene'].title), 10)
                lst = _getList(data[1]['persons'], data[1]['tops'])
                tmp.append(f"{sc:\u3000<10}|{lst}")
        return [f"# {title}\n", "## Persons\n", head] + tmp

    @classmethod
    def toLinescaleOfStage(cls, title: str, src: list, areas: list, basedate: datetime.date) -> list:
        tmp = []
        stages = []
        oldarea = ""
        oldplace = ""
        before = basedate
        past = datetime.time(0,0,0)
        for data in src:
            if DataType.SCENE_SETTING is data[0]:
                stages.append(data[1]["stage"])
        stagelist = sorted(list(set([v.name for v in stages])))
        def _getArea(stage, area):
            idx = 0
            for a in areas:
                if a.tag == stage.area or a.tag == area.tag:
                    return idx
                idx += 1
            return idx
        def _getIcon(stage, area):
            if stage.area in __DRIVE_STAGE__ or area.tag == "Drive":
                return "🚗"
            elif stage.name in __WALK_STAGE__:
                return "🚶"
            else:
                return "🏠"
        def _chopped(v):
            if len(v) >= 4:
                return v[0:4]
            else:
                return f"{v:\u3000<4}"
        def _daydelta(day: datetime.date, bef:datetime.date,
                time: datetime.time, past: datetime.time):
            if day.year > bef.year:
                return "▼"
            elif day.year < bef.year:
                return "▲"
            elif day.month > bef.month:
                return "▽"
            elif day.month < bef.month:
                return "△"
            elif day.day > bef.day:
                return "↓"
            elif day.day < bef.day:
                return "↑"
            elif time.hour > past.hour:
                return "︙"
            elif time.minute > past.minute:
                return "︰"
            else:
                return "⊥"
        heads = "|".join([f"{strEllipsis(v.name, 8, ''):\u3000<8}" for v in areas]) + "|その他"
        shortheads = "".join([v.name[0] for v in areas])
        for data in src:
            if DataType.HEAD is data[0]:
                tmp.append(f"\n{data[1]}\n")
                _ = "　"*13 + " "*10
                tmp.append(f"{_}|{shortheads}")
            elif DataType.SCENE_SETTING is data[0]:
                icon = _getIcon(data[1]['stage'], data[1]['area'])
                num = _getArea(data[1]["stage"], data[1]['area'])
                pattern = "　"
                delta = _daydelta(data[1]['day'], before, data[1]['time'].data, past)
                before = data[1]['day']
                past = data[1]['time'].data
                idt = pattern * num + f"{delta}" + pattern * (len(stagelist) - num - 1)
                stage = strEllipsis(data[1]['stage'].name, 8) if oldplace != data[1]['stage'].name else "　…"
                oldplace = data[1]['stage'].name
                timename = strEllipsis(data[1]['time'].name, 4, "※")
                tmp.append(f"{icon}{stage:\u3000<8}{timename:\u3000<4}{data[1]['day']}|{idt}")
        return [f"# {title}\n", "## Areas\n", f"{heads}"] + tmp

    @classmethod
    def toOutline(cls, title: str, src: list) -> list:
        tmp = []
        src_cmt = []
        isComment = False
        for data in src:
            if isComment:
                src_cmt.append(data)
            elif DataType.HEAD is data[0]:
                tmp.append(data[1])
            elif DataType.DATA_STR is data[0]:
                tmp.append(f"\t{data[1]}")
            elif DataType.TAG is data[0]:
                if "hr" == data[1]:
                    tmp.append("--------"*8)
            elif DataType.COMMAND is data[0] and "all" == data[1]:
                isComment = True
        for data in cls.srcConvertedTitleWithNum(src_cmt):
            if data[0] in TitleLike:
                tmp.append(data[1])
            if DataType.HEAD is data[0]:
                tmp.append(data[1])
            elif DataType.DATA_STR is data[0]:
                tmp.append(f"\t{data[1]}")
            elif DataType.TAG is data[0]:
                if "hr" == data[1]:
                    tmp.append("--------"*8)
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
    def toListStage(cls, title: str, src: list) -> list:
        tmp = []
        for data in src:
            if DataType.DATA_DICT is data[0]:
                for k,v in data[1].items():
                    tmp.append(f"- {k:<24} | {v.name:\u3000<16} | {v.area:\u3000<12} | {v.info}")
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
