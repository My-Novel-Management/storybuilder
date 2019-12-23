# -*- coding: utf-8 -*-
"""For format class.
"""
from itertools import chain
from . import assertion
from .scene import ScenarioType
from .strutils import str_duplicated_chopped


class Formatter(object):
    """The output format tools.
    """

    # methods
    def toActionPercentInfo(self, total: int, data: dict, prefix: str, idt: int=0,
            isHead: bool=True) -> list:
        heads = ""
        vals = ""
        indent1 = " " * 4 * (idt)
        indent2 = " " * 4 * (idt + 1)
        for k,v in data.items():
            heads += f"{k:>6} /"
            vals += f"{v:>5.2f}% /"
        heads = f"{indent2}- {heads}\n" if isHead else ""
        return [f"{indent1}* {prefix}: {total}",
                f"{heads}{indent2}- {vals}",
                ]

    def toActionPercentInfoEachScenes(self, totals:list, data: list) -> list:
        def _level(v):
            if "Ch" in v: return 0
            elif "Ep" in v: return 1
            else: return 2
        return list(chain.from_iterable(
            self.toActionPercentInfo(t, v[1], v[0], _level(v[0]), False) for t,v in zip(totals, data)
            ))

    def toCharactersInfo(self, data: dict, prefix: str=None, idt: int=0) -> list:
        desc_total = data["desc_total"]
        outline_total = data["outline_total"]
        estimated = data["estimated"]
        desc_rows = data["desc_rows"]
        outline_rows = data["outline_rows"]
        columns = data["base_columns"]
        rows = data["base_rows"]
        desc_pp = desc_rows / rows
        outline_pp = outline_rows / rows
        indent = " " * 4 * idt
        title = f"{indent}* {prefix}" if prefix else "* Characters"
        return [title \
                + f" - {desc_total}c [{desc_pp:0.2f}p ({desc_rows:0.2f}ls)]" \
                + f" / Outline: {outline_total}c [{outline_pp:0.2f}p ({outline_rows:0.2f})ls]" \
                + f"- Estimated: {estimated}c",
                ]

    def toCharactersInfoEachScenes(self, data: list) -> list:
        tmp = []
        idt = 0
        for v in data:
            if "Ch" in v[0]:
                idt = 0
            elif "Ep" in v[0]:
                idt = 1
            else:
                idt = 2
            tmp.append(self.toCharactersInfo(v[1], v[0], idt))
        return list(chain.from_iterable(tmp))

    def toDescriptions(self, data: list) -> list:
        def _conv(v):
            if "###" in v: return f"\n{v}\n"
            elif "##" in v: return f"\n{v}\n"
            elif "#" in v: return f"{v}\n"
            elif "**" in v: return f"\n{v}\n"
            else: return v
        return [_conv(v) for v in data]

    def toDescriptionsAsEstar(self, data: list) -> list:
        tmp = []
        indialogue = False
        for v in assertion.is_list(data):
            if "#" in v or "**" in v:
                tmp.append(v)
            else:
                cur = v.startswith(('「', '『'))
                pre = "" if indialogue == cur else "\n"
                tmp.append(pre + v + "\n")
                indialogue = cur
        return tmp

    def toDescriptionsAsLayer(self, data: list) -> list:
        tmp = []
        title = data[0][1] if "__TITLE__" == assertion.is_list(data)[0][0] else "no title"
        layers = []
        for v in data[1:]:
            head, lname = v[0].split(":")
            layers.append(lname)
        layers_sorted = sorted(list(set(layers)))
        tmp.append(f"{title}\n")
        for k in layers_sorted:
            tmp.append("--------"*8)
            tmp.append(f"## {k}\n")
            head_title = ""
            for v in data[1:]:
                head, lname = v[0].split(":")
                if lname == k:
                    if head_title != head:
                        tmp.append(f"* {head}")
                        head_title = head
                    tmp.append(f"    - {v[1]}")
        return tmp

    def toDescriptionsAsSmartphone(self, data: list) -> list:
        tmp = []
        for v in assertion.is_list(data):
            if "#" in v or "**" in v:
                tmp.append(v)
            else:
                tmp.append(f"{v}\n")
        return tmp

    def toDescriptionsAsWeb(self, data: list) -> list:
        tmp = []
        inDialogue = False
        for v in assertion.is_list(data):
            if "#" in v or "**" in v:
                tmp.append(v)
            else:
                cur = v.startswith(('「', '『'))
                pre = "" if inDialogue == cur else "\n"
                tmp.append(pre + v)
                inDialogue = cur
        return tmp

    def toDialoguesInfo(self, data: list) -> list:
        tmp = []
        for v in data:
            tmp.append(f"* {v[0]}")
            for d in v[1]:
                tmp.append(f"    - {d}")
        return tmp

    def toFlagsInfo(self, data: list) -> list:
        tmp = []
        flags = [v for v in data if not v.isDeflag]
        deflags = [v for v in data if v.isDeflag]
        tmp.append("* Flags")
        for v in flags:
            tmp.append(f"    + {v.info}")
        tmp.append("* Deflags")
        for v in deflags:
            tmp.append(f"    - {v.info}")
        return tmp

    def toLayersInfo(self, data: list) -> list:
        tmp = []
        for v in data:
            if "#" in v:
                tmp.append(v)
            else:
                tmp.append(f"- {v}")
        return tmp

    def toOutlines(self, data: list) -> list:
        tmp = []
        sc_head = ""
        inEpisode = False
        inScene = False
        for v in assertion.is_list(data):
            if "###" in v:
                tmp.append(f"\n{v}\n")
                inEpisode = True
            elif "##" in v:
                tmp.append(f"\n{v}\n")
            elif "#" in v:
                tmp.append(f"{v}\n")
            elif "**" in v:
                sc_head = v
                inScene = True
            elif inEpisode:
                tmp.append(f"\t{v}\n")
                inEpisode = False
            elif inScene:
                tmp.append(f"- {sc_head}: {v}")
                inScene = False
            else:
                tmp.append(v)
        return tmp

    def toOutlinesAsLayer(self, data: list) -> list:
        tmp = []
        title = data[0][1] if "__TITLE__" == assertion.is_list(data)[0][0] else "no title"
        layers = []
        for v in data[1:]:
            head, lname = v[0].split(":")
            layers.append(lname)
        layers_sorted = sorted(list(set(layers)))
        tmp.append(f"{title}\n")
        for k in layers_sorted:
            tmp.append("--------"*8)
            tmp.append(f"## {k}\n")
            head_title = ""
            for v in data[1:]:
                head, lname = v[0].split(":")
                if lname == k:
                    if head_title != head:
                        tmp.append(f"* {head}")
                        head_title = head
                    tmp.append(f"    - {v[1]}")
        return tmp

    def toScenarios(self, data: list) -> list:
        tmp = []
        for v in assertion.is_list(data):
            if v[0] is ScenarioType.TITLE:
                if "###" in v[1]:
                    tmp.append(f"\n{v[1]}\n")
                elif "##" in v[1]:
                    tmp.append(f"\n{v[1]}\n")
                elif "#" in v[1]:
                    tmp.append(f"{v[1]}\n")
                elif "**" in v[1]:
                    tmp.append(f"\n{v[1]}\n")
            elif v[0] is ScenarioType.PILLAR:
                stage, day, time = v[1].split(":")
                tmp.append(f"○{stage}（{time}）- {day}")
            elif v[0] is ScenarioType.DIRECTION:
                tmp.append(str_duplicated_chopped(f"　　{v[1]}。"))
            elif v[0] is ScenarioType.DIALOGUE:
                subject, dial = v[1].split(":")
                tmp.append(f"{subject}「{dial}」")
            elif v[0] is ScenarioType.TAG:
                if v[1]:
                    tmp.append(v[1])
            elif v[0] is ScenarioType.EFFECT:
                tmp.append(v[1])
            else:
                raise AssertionError("Not reachable value: ", v[0])
        return tmp

    def toScenariosAsLayer(self, data: list) -> list:
        tmp = []
        title = data[0][3] if "__TITLE__" == data[0][0] else "no title"
        layers = []
        pillars = []
        for v in data[1:]:
            head, lname = v[0].split(":")
            layers.append(lname)
            if not v[1] in pillars:
                pillars.append(v[1])
        layers_sorted = sorted(list(set(layers)))
        tmp.append(f"{title}\n")
        for k in layers_sorted:
            tmp.append("--------"*8)
            tmp.append(f"## {k}\n")
            for p in pillars:
                stage, day, time = p.split(":")
                isFirst = False
                for v in data[1:]:
                    head, lname = v[0].split(":")
                    if not isFirst:
                        tmp.append(f"{head}: {stage}（{time}）- {day}")
                        isFirst = True
                    if k == lname and v[1] == p:
                        if v[2] is ScenarioType.DIRECTION:
                            tmp.append(f"\t{v[3]}。")
                        elif v[2] is ScenarioType.DIALOGUE:
                            subject, dial = v[3].split(":")
                            tmp.append(f"{subject}「{dial}」")
                        else:
                            tmp.append(v[3])
        return tmp

    ## privates
    def _lineBreak(self) -> list:
        return ["--------" * 8]
