# -*- coding: utf-8 -*-
"""Define tool for format
"""
## public libs
from itertools import chain
import textwrap
## local libs
from utils import assertion
## local files
from builder import ActType, TagType
from builder.action import Action
from builder.datapack import DataPack
from builder.extractor import Extractor
from builder.item import Item
from builder.word import Word


class Formatter(object):
    """The tool class for format
    """

    ## methods
    @classmethod
    def toConte(cls, title: str, src: list) -> list:
        tmp = []
        ch_num, ep_num, sc_num = 1,1,1
        def _getMsgAndComment(act: Action):
            tmp = Extractor.getDirectionsFrom(act)
            msg = tmp[0] if tmp else ""
            cmt = "/".join(tmp[1:]) if len(tmp) > 1 else ""
            return msg, cmt
        def _conteFrom(doing, sound, pic, act):
            sd = textwrap.wrap(f"{sound:\u3000<20}", 20)
            tmp = "".join(sd[0][0:19]) + "…" if len(sound) > 20 else f"{sound:\u3000<20}"
            return f"{doing}|{tmp}|{pic:\u3000<20}|{act:\u3000<20}"
        for v in src:
            assertion.isInstance(v, DataPack)
            if "title" in v.head:
                if "story" in v.head:
                    tmp.append(f"# {v.body}\n")
                elif "chapter" in v.head:
                    tmp.append(f"\n## Ch-{ch_num}: {v.body}\n")
                    ch_num += 1
                elif "episode" in v.head:
                    tmp.append(f"\n### Ep-{ep_num}: {v.body}\n")
                    ep_num += 1
                elif "scene" in v.head:
                    tmp.append(f"\n** Sc-{sc_num}: {v.body} **\n")
                    sc_num += 1
            elif "setting" in v.head:
                camera, stage, day, time = v.body.split(":")
                tmp.append(f"○{stage}（{time}） - {day}＜{camera}＞")
            else:
                h, name = v.head.split(":")
                act = v.body
                ## Words
                if ActType.TALK.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    shots = Extractor.getShotsFrom(act)
                    dialogues = "。".join(chain.from_iterable([v.infos for v in shots]))
                    tmp.append(_conteFrom("TA", dialogues, name, f"{msg}/{cmt}"))
                elif ActType.THINK.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    tmp.append(_conteFrom("TH", f"（{msg}", name, cmt))
                elif ActType.EXPLAIN.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    tmp.append(_conteFrom("EX", f"＃{msg}", name, cmt))
                ## Exists
                elif ActType.BE.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    tmp.append(_conteFrom("BE", "", f"［{name}］", f"{msg}/{cmt}"))
                elif ActType.DESTROY.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    tmp.append(_conteFrom("DE", "", f"＿［{name}］", f"{msg}/{cmt}"))
                elif ActType.WEAR.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    items = [v for v in Extractor.getObjectsFrom(act) if isinstance(v, (Item, Word))]
                    base = f"{name}" + "".join(f"｛{v.name}｝" for v in items) + f"｛{msg}｝"
                    tmp.append(_conteFrom("WE", "", base, f"{cmt}"))
                elif ActType.TAKEOFF.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    items = [v for v in Extractor.getObjectsFrom(act) if isinstance(v, (Item, Word))]
                    base = f"{name}＿" + "".join(f"｛{v}｝" for v in items) + f"｛{msg}｝"
                    tmp.append(_conteFrom("OF", "", base, f"{cmt}"))
                elif ActType.HAVE.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    items = [v for v in Extractor.getObjectsFrom(act) if isinstance(v, (Item, Word))]
                    base = f"{name}" + "".join([f"［{v.name}］" for v in items])
                    tmp.append(_conteFrom("HA", "", base, f"{msg}/{cmt}"))
                elif ActType.DISCARD.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    items = [v for v in Extractor.getObjectsFrom(act) if isinstance(v, (Item, Word))]
                    base = f"{name}" + "".join([f"［{v.name}］" for v in items])
                    tmp.append(_conteFrom("DI", "", base, f"{msg}/{cmt}"))
                ## Controls
                elif ActType.MOVE.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    base = f"↓{name}"
                    tmp.append(_conteFrom("MO", "", base, f"{msg}/{cmt}"))
                elif ActType.GO.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    base = f"←［{name}］"
                    tmp.append(_conteFrom("GO", "", base, f"{msg}/{cmt}"))
                elif ActType.COME.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    base = f"→［{name}］（{msg}）"
                    tmp.append(_conteFrom("CO", "", base, f"{msg}/{cmt}"))
                ## Effects
                elif ActType.HEAR.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    tmp.append(_conteFrom("HE", f"♪{msg}", name, cmt))
                elif ActType.LOOK.name in h:
                    msg, cmt = _getMsgAndComment(act)
                    base = f"{name}｛{msg}｝"
                    tmp.append(_conteFrom("LO", "", base, cmt))
                ## Acts
                else:
                    msg, cmt = _getMsgAndComment(act)
                    tmp.append(_conteFrom("AC", "", name, f"{msg}/{cmt}"))
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
        for v in src:
            assertion.isInstance(v, DataPack)
            if "title" in v.head:
                if "story" in v.head:
                    tmp.append(f"# {v.body}\n")
                elif "chapter" in v.head:
                    tmp.append(f"\n## Ch-{ch_num}: {v.body}\n")
                    ch_num += 1
                elif "episode" in v.head:
                    tmp.append(f"\n### Ep-{ep_num}: {v.body}\n")
                    ep_num += 1
                elif "scene" in v.head:
                    tmp.append(f"\n** Sc-{sc_num}: {v.body} **\n")
                    sc_num += 1
            else:
                if "dialogue" == v.head:
                    if inDialogue: # D-D
                        tmp.append(f"{dd_sp}「{v.body}」")
                    else: # L-D
                        tmp.append(f"{ld_sp}「{v.body}」")
                        inDialogue = True
                else:
                    if inDialogue: # D-L
                        tmp.append(f"{dl_sp}　{v.body}")
                        inDialogue = False
                    else: # L-L
                        tmp.append(f"{ll_sp}　{v.body}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toGeneralInfo(cls, title: str, src: list) -> list:
        # TODO? Shotのみでなく、Directionそのものの文字数も参考値出すか？
        total, manupaper, rows, columns = 0, 0, 0, 0
        chapters, episodes, scenes, actions = 0,0,0, 0
        act_total = 0
        acttypes = []
        for v in src:
            if assertion.isInstance(v, DataPack).head == "total":
                total = v.body
            elif v.head == "manupaper":
                manupaper = v.body
            elif v.head == "rows":
                rows = v.body
            elif v.head == "columns":
                columns = v.body
            elif v.head == "chapters":
                chapters = v.body
            elif v.head == "episodes":
                episodes = v.body
            elif v.head == "scenes":
                scenes = v.body
            elif v.head == "actions":
                actions = v.body
            elif "acttype" in v.head:
                if "total" in v.head:
                    act_total = v.body
                else:
                    acttypes.append(v.body)
        papers = manupaper / rows if rows else 0
        talk_idx = 0
        for v in ActType:
            if v is ActType.TALK:
                break
            talk_idx += 1
        talk_percent = acttypes[talk_idx] / sum(acttypes) *100 if act_total else 0
        action_info = ["--------" * 8, "\n",
                f"## Action info: {act_total} / Dialogues: {talk_percent:.2f}%",
                ] + sorted([f"- {t.name}: {v/act_total*100:.2f}%" for t, v in zip(ActType, acttypes)])
        res = [f"# {title}\n",
                f"## Total: {total}c / [{papers:.2f}p ({manupaper:.2f}ls) ]",
                f"## Chapters: {chapters} / Episodes: {episodes} / Scenes: {scenes} / Actions: {actions}",
                ]
        if act_total:
            return res + action_info
        else:
            return res

    @classmethod
    def toKanjiInfo(cls, title: str, src: list) -> list:
        total, kanji = 0, 0
        for v in src:
            if "total" in assertion.isInstance(v, DataPack).head:
                total = v.body
            elif "kanji" in v.head:
                kanji = v.body
        percent = kanji / total *100 if total else 0
        return [f"# {title}\n",
                f"## Kanji: {percent:.2f}% - {kanji}c / {total}c"]

    @classmethod
    def toOutline(cls, title: str, src: list) -> list:
        tmp = []
        ch_num, ep_num, sc_num = 1,1,1
        for v in src:
            assertion.isInstance(v, DataPack)
            if "title" in v.head:
                if "story" in v.head:
                    tmp.append(f"# {v.body}\n")
                elif "chapter" in v.head:
                    tmp.append(f"\n## Ch-{ch_num}: {v.body}\n")
                    ch_num += 1
                elif "episode" in v.head:
                    tmp.append(f"\n## Ep-{ep_num}: {v.body}\n")
                    ep_num += 1
                elif "scene" in v.head:
                    tmp.append(f"\n** Sc-{sc_num}: {v.body} **\n")
                    sc_num += 1
            else:
                if v.body:
                    tmp.append(f"    - {v.body}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toLayerInfo(cls, title: str, src: list) -> list:
        tmp = []
        ch_num, ep_num, sc_num = 1,1,1
        count, dialogues = 0, 0
        for v in src:
            if "title" in assertion.isInstance(v, DataPack).head:
                if "story" in v.head:
                    tmp.append(f"# {v.body}\n")
                elif "chapter" in v.head:
                    tmp.append(f"* [in Ch-{ch_num}]: {v.body}")
                    ch_num += 1
                elif "episode" in v.head:
                    tmp.append(f"* [in Ep-{ep_num}]: {v.body}")
                    ep_num += 1
                elif "scene" in v.head:
                    tmp.append(f"* [in Sc-{sc_num}]: {v.body}")
                    sc_num += 1
            elif "head" in v.head:
                tmp.append(f"\n## layer of {v.body}\n")
            elif "hr" == v.head:
                tmp.append(f"{'--------' * 8}\n")
            elif "dialogue" in v.head:
                tmp.append(f"    - 「{v.body}」")
                dialogues += 1
            else:
                if v.body:
                    tmp.append(f"    - {v.body}")
                    count += 1
        return [f"# {title}\n",
                f"\n- Total: {count} / Dialogues: {dialogues}\n",
                ] + tmp

    @classmethod
    def toListInfo(cls, title: str, src: list) -> list:
        tmp = []
        for v in src:
            p = v.body
            tmp.append(f"- {v.head:<16} | {p.name:\u3000<10} | {p.note}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toListDays(cls, title: str, src: list) -> list:
        tmp = []
        for v in src:
            p = v.body
            tmp.append(f"- {v.head:<16} | {p.name:\u3000<10} | {p.date}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toListPersons(cls, title: str, src: list) -> list:
        tmp = []
        for v in src:
            p = v.body
            full = p.fullname.replace(',','　')
            tmp.append(f"- {v.head:<16} | {p.name:\u3000<8} | {full:\u3000<10} | {p.age}歳 | {p.sex} | {p.job} | {p.note}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toListTimes(cls, title: str, src: list) -> list:
        tmp = []
        for v in src:
            p = v.body
            tmp.append(f"- {v.head:<16} | {p.name:\u3000<10} | {p.time}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toWordClassInfo(cls, title: str, src: list) -> list:
        tmp = []
        for v in src:
            if "head" in v.head:
                tmp.append(f"\n## {v.body}\n")
            elif "count" in v.head:
                tmp.append(f"- {v.body}")
        return [f"# {title}\n",
                ] + tmp
