# -*- coding: utf-8 -*-
"""Define tool for format
"""
## public libs
## local libs
from utils import assertion
## local files
from builder import ActType, TagType
from builder.datapack import DataPack


class Formatter(object):
    """The tool class for format
    """

    ## methods
    @classmethod
    def toConte(cls, title: str, src: list) -> list:
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
                    tmp.append(f"\n### Ep-{ep_num}: {v.body}\n")
                    ep_num += 1
                elif "scene" in v.head:
                    tmp.append(f"\n** Sc-{sc_num}: {v.body} **\n")
                    sc_num += 1
            elif "setting" in v.head:
                camera, stage, day, time = v.body.split(":")
                tmp.append(f"○{stage}（{time}） - {day}/{camera}")
            else:
                h, name = v.head.split(":")
                doing, body = v.body.split(":")
                if f"{ActType.TALK.name}" in h:
                    tmp.append(f"{name}「{body}」")
                elif f"{ActType.THINK.name}" in h:
                    tmp.append(f"{name}（{body}）")
                elif f"{ActType.BE.name}" in h:
                    tmp.append(f"    + [ {name} ] | {body}")
                elif f"{ActType.DESTROY}" in h:
                    tmp.append(f"    - [ {name} ] | {body}")
                elif f"{ActType.WEAR.name}" in h:
                    tmp.append(f"    + [ {name} ({body}) ]")
                elif f"{ActType.TAKEOFF.name}" in h:
                    tmp.append(f"    - [ {name} ({body}) ]")
                elif f"{ActType.HAVE.name}" in h:
                    tmp.append(f"    + [ {name} [{body}] ]")
                elif f"{ActType.DISCARD.name}" in h:
                    tmp.append(f"    - [ {name} [{body}] ]")
                elif f"{ActType.MOVE.name}" in h:
                    tmp.append(f"    <{name}> | {body}")
                elif f"{ActType.GO.name}" in h:
                    tmp.append(f"    - <<{name} | {body}")
                elif f"{ActType.COME.name}" in h:
                    tmp.append(f"    + >> [ {name} ] | {body}")
                elif f"{ActType.HEAR}" in h:
                    tmp.append(f"    ♪ {name}:{body}")
                else:
                    tmp.append(f"    {name}:{body}")
        return [f"# {title}\n",
                ] + tmp

    @classmethod
    def toDescription(cls, title: str, src: list) -> list:
        tmp = []
        ch_num, ep_num, sc_num = 1, 1, 1
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
                    tmp.append(f"「{v.body}」")
                else:
                    tmp.append(f"　{v.body}")
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
    def toWordClassInfo(cls, title: str, src: list) -> list:
        tmp = []
        for v in src:
            if "head" in v.head:
                tmp.append(f"\n## {v.body}\n")
            elif "count" in v.head:
                tmp.append(f"- {v.body}")
        return [f"# {title}\n",
                ] + tmp
