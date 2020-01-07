# -*- coding: utf-8 -*-
"""Define tool for check a story
"""
## public libs
## local libs
from utils import assertion
## local files
from builder import ActType, TagType, MetaType
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.extractor import Extractor
from builder.metadata import MetaData
from builder.person import Person
from builder.scene import Scene
from builder.story import Story


## define types
TestLike = (MetaType.TEST_EXISTS_THAT, MetaType.TEST_HAS_THAT)


## define class
class Checker(object):
    """The tool class for check.
    """
    @classmethod
    def validateConditions(cls, src: Story) -> bool:
        msg = []
        status = set()
        def _haveStr(ac, it):
            return f"{ac.subject.name}__{it.name}"
        for ch in src.data:
            for ep in ch.data:
                for sc in ep.data:
                    sc_status = set()
                    for ac in sc.data:
                        ## object control
                        if ac.act_type in (ActType.BE, ActType.COME):
                            status = status | {ac.subject.name}
                            sc_status = sc_status | {ac.subject.name}
                        elif ActType.HAVE is ac.act_type:
                            for it in Extractor.objectsFrom(ac):
                                status = status | {it.name, _haveStr(ac, it)}
                                sc_status = sc_status | {it.name, _haveStr(ac, it)}
                        elif ac.act_type in (ActType.DESTROY, ActType.GO):
                            status = status - {ac.subject.name}
                            sc_status = sc_status - {ac.subject.name}
                        elif ActType.DISCARD is ac.act_type:
                            for it in Extractor.objectsFrom(ac):
                                status = status - {it.name, _haveStr(ac, it)}
                                sc_status = sc_status - {it.name, _haveStr(ac, it)}
                        ## meta check
                        metas = Extractor.metadataFrom(ac)
                        for meta in metas:
                            if MetaType.TEST_EXISTS_THAT is meta.data:
                                if not ac.subject.name in status:
                                    msg.append(f"No exists {ac.subject.name} [in story]")
                                if "scene" in meta.note and not ac.subject.name in sc_status:
                                    msg.append(f"No exists {ac.subject.name} [in {sc.title}]")
                            elif MetaType.TEST_HAS_THAT is meta.data:
                                for it in Extractor.objectsFrom(ac):
                                    if not _haveStr(ac, it) in status:
                                        msg.append(f"{ac.subject.name} No have {it.name} [in story]")
                                    if "scene" in meta.note and not _haveStr(ac, it) in sc_status:
                                        msg.append(f"{ac.subject.name} No have {it.name} [in {sc.title}]")
        if msg:
            for m in msg:
                print(f"!! {m} !!")
            return False
        else:
            return True

    @classmethod
    def validateObjects(cls, src: Story) -> bool:
        msg = []
        for ch in src.data:
            for ep in ch.data:
                for sc in ep.data:
                    status = {}
                    for ac in sc.data:
                        if ActType.META is ac.act_type:
                            continue
                        elif ac.act_type in (ActType.BE, ActType.COME):
                            status[ac.subject.name] = ac.itemCount
                        elif ActType.HAVE is ac.act_type:
                            objects = Extractor.itemsFrom(ac)
                            for it in objects:
                                status[it.name] = ac.itemCount
                        elif ac.act_type in (ActType.DESTROY, ActType.GO):
                            if not ac.subject.name in status:
                                msg.append(f"Missing {ac.subject.name} [in {sc.title}]")
                            elif status[ac.subject.name] <= 0:
                                msg.append(f"Lacking {ac.subject.name} [in {sc.title}]")
                            status[ac.subject.name] -= ac.itemCount
                        elif ActType.DISCARD is ac.act_type:
                            objects = Extractor.itemsFrom(ac)
                            for it in objects:
                                if it.name in status:
                                    msg.append(f"Missing {it.name} [in {sc.title}]")
                                elif status[it.name] <= 0:
                                    msg.append(f"Lacking {it.name} [in {sc.title}]")
                                status[it.name] -= ac.itemCount
                        elif ac.act_type in (ActType.ACT, ActType.LOOK, ActType.TALK, ActType.THINK, ActType.VOICE):
                            if not ac.subject.name in status:
                                msg.append(f"Missing {ac.subject.name} [in {sc.title}]")
                            elif status[ac.subject.name] <= 0:
                                msg.append(f"Lacking {ac.subject.name} [in {sc.title}]")
        if msg:
            for m in msg:
                print(f"!! {m} !!")
            return False
        else:
            return True
