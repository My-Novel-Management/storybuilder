# -*- coding: utf-8 -*-
"""For format class.
"""
from . import assertion
from .scene import ScenarioType
from .strutils import str_duplicated_chopped


class Formatter(object):
    """The output format tools.
    """

    # methods
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
            for v in data[1:]:
                head, lname = v[0].split(":")
                if lname == k:
                    tmp.append(f"{head}: {v[1]}")
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
            for v in data[1:]:
                head, lname = v[0].split(":")
                if lname == k:
                    tmp.append(f"{head}: {v[1]}")
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
