# -*- coding: utf-8 -*-
"""For format class.
"""
from . import assertion


class Formatter(object):
    """The output format tools.
    """

    # methods
    def asDescription(self, data: list, format_type: str):
        if format_type in ("estar",):
            return _descriptionsAsEstar(data)
        elif format_type in ("smartphone", "phone", "smart"):
            return _descriptionsAsSmartphone(data)
        elif format_type in ("web",):
            return _descriptionsAsWebnovel(data)
        else:
            return data

    def asLayer(self, data: list, is_outline: bool):
        from .action import Action, TagAction, ActType
        tmp = []
        datahead = data[0]
        layers = sorted(list(set([v[0] for v in data[1:]])))
        def _conv_talk(act: Action, base: str):
            return f"_「{base}」_" if act.act_type is ActType.TALK else base
        def _conv(act: [Action, TagAction], is_outline: bool):
            # TODO: tag
            if isinstance(act, TagAction):
                return ""
            else:
                if is_outline:
                    return _conv_talk(act, act.outline)
                else:
                    return _conv_talk(act, "".join(act.description.descs)) if act.description.descs else ""
        def _convert(data: tuple, layer: str, is_outline: bool):
            if layer == data[0]:
                tmp1 = _conv(v[2], is_outline)
                return f"{data[1]}: {tmp1}" if tmp1 else ""
            else:
                return ""
        for l in layers:
            tmp.append("--------" * 9 + f"\n## {l}\n")
            for v in data[1:]:
                tmp.append(_convert(v, l, is_outline))
        return [datahead] + [v for v in tmp if v]

    def asOutline(self, data: list):
        tmp = []
        for v in data:
            if "###" in v[0]:
                tmp.append(f"{v[0]}\n\n\t{v[1]}")
            elif "#" in v[0]:
                tmp.append(f"{v[0]}")
            else:
                tmp.append(f"- 「{v[0]}」: {v[1]}")
        return tmp

    def asScenario(self, data: list):
        from .scene import ScenarioType
        tmp = []
        for v in data:
            if v[0] is ScenarioType.DIRECTION:
                tmp.append("　　" + v[1])
            else:
                tmp.append(v[1])
        return tmp

## privates
def _descriptionsAsEstar(data: list) -> list:
    tmp = []
    inDialogue = False
    for v in assertion.is_list(data):
        cur = v.startswith(('「', '『'))
        pre = "" if inDialogue == cur else "\n"
        tmp.append(pre + v + "\n")
        inDialogue = cur
    return tmp

def _descriptionsAsSmartphone(data: list) -> list:
    return [f"{v}\n" for v in assertion.is_list(data)]

def _descriptionsAsWebnovel(data: list) -> list:
    tmp = []
    inDialogue = False
    for v in assertion.is_list(data):
        cur = v.startswith(('「', '『'))
        pre = "" if inDialogue == cur else "\n"
        tmp.append(pre + v)
        inDialogue = cur
    return tmp

