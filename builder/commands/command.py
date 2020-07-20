# -*- coding: utf-8 -*-
'''
Story Command list
==================
'''

from __future__ import annotations

__all__ = ('SCmd',)


from enum import Enum, auto
from builder.utils import assertion


class SCmd(Enum):
    ''' Story command enumerate.
    '''

    #
    # subjects
    #

    BE = auto()
    COME = auto()
    DO = auto()
    EXPLAIN = auto()
    GO = auto()
    HEAR = auto()
    LOOK = auto()
    TALK = auto()
    THINK = auto()
    VOICE = auto()
    WEAR = auto()

    #
    # scene control
    #

    CHANGE_CAMEARA = auto()
    CHANGE_STAGE = auto()
    CHANGE_DATE = auto()
    CHANGE_TIME = auto()
    ELAPSE_DAY = auto()
    ELAPSE_TIME = auto()
    PUT_OBJECT = auto()

    #
    # tags
    #

    TAG_BR = auto()
    TAG_COMMENT = auto()
    TAG_HR = auto()
    TAG_SYMBOL = auto()
    TAG_TITLE = auto()

    #
    # plot info
    #

    PLOT_NOTE = auto()
    PLOT_MOTIF = auto()
    PLOT_FORESHADOW = auto()
    PLOT_PAYOFF = auto()
    PLOT_SETUP = auto()
    PLOT_DEVELOP = auto()
    PLOT_RESOLVE = auto()
    PLOT_TURNPOINT = auto()

    #
    # meta
    #

    INFO_DATA = auto()
    INFO_CONTENT = auto()
    INFO_STORY = auto()
    END_CHAPTER = auto()
    END_EPISODE = auto()
    END_SCENE = auto()
    END_MATERIAL = auto()
    HEAD_CHAPTER = auto()
    HEAD_EPISODE = auto()
    HEAD_SCENE = auto()
    HEAD_MATERIAL = auto()
    THEN = auto()

    @classmethod
    def get_all(cls) -> list:
        return [cls.BE, cls.COME, cls.DO, cls.EXPLAIN, cls.GO,
                cls.HEAR, cls.LOOK, cls.THINK, cls.WEAR,
                cls.TALK, cls.VOICE,
                cls.CHANGE_CAMEARA, cls.CHANGE_DATE, cls.CHANGE_STAGE,
                cls.CHANGE_TIME,
                cls.ELAPSE_DAY, cls.ELAPSE_TIME,
                cls.END_CHAPTER, cls.END_EPISODE, cls.END_SCENE, cls.END_MATERIAL,
                cls.HEAD_CHAPTER, cls.HEAD_EPISODE, cls.HEAD_SCENE, cls.HEAD_MATERIAL,
                cls.PLOT_NOTE, cls.PLOT_MOTIF,
                cls.PLOT_FORESHADOW, cls.PLOT_PAYOFF,
                cls.PLOT_SETUP, cls.PLOT_DEVELOP, cls.PLOT_RESOLVE, cls.PLOT_TURNPOINT,
                cls.INFO_DATA, cls.INFO_CONTENT, cls.INFO_STORY,
                cls.PUT_OBJECT,
                cls.TAG_BR, cls.TAG_COMMENT, cls.TAG_HR, cls.TAG_SYMBOL,
                cls.TAG_TITLE,
                cls.THEN,
                ]

    @classmethod
    def get_all_actions(cls) -> list:
        return [cls.BE, cls.DO, cls.EXPLAIN, cls.THINK,
                cls.TALK, cls.VOICE,
                cls.COME, cls.GO,
                cls.HEAR, cls.LOOK, cls.WEAR]

    @classmethod
    def get_normal_actions(cls) -> list:
        return [cls.BE, cls.DO, cls.EXPLAIN, cls.THINK,
                cls.COME, cls.GO,
                cls.HEAR, cls.LOOK, cls.WEAR]

    @classmethod
    def get_dialogue_actions(cls) -> list:
        return [cls.TALK, cls.VOICE]

    @classmethod
    def get_informations(cls) -> list:
        return [cls.INFO_DATA, cls.INFO_CONTENT, cls.INFO_STORY]

    @classmethod
    def get_end_of_containers(cls) -> list:
        return [cls.END_CHAPTER, cls.END_EPISODE, cls.END_SCENE,
                cls.END_MATERIAL]

    @classmethod
    def get_head_of_containers(cls) -> list:
        return [cls.HEAD_CHAPTER, cls.HEAD_EPISODE, cls.HEAD_SCENE, cls.HEAD_MATERIAL]

    @classmethod
    def get_plot_infos(cls) -> list:
        return [cls.PLOT_NOTE, cls.PLOT_MOTIF,
                cls.PLOT_FORESHADOW, cls.PLOT_PAYOFF,
                cls.PLOT_SETUP, cls.PLOT_DEVELOP, cls.PLOT_RESOLVE, cls.PLOT_TURNPOINT]

    @classmethod
    def get_plot_structs(cls) -> list:
        return [cls.PLOT_SETUP, cls.PLOT_DEVELOP, cls.PLOT_RESOLVE, cls.PLOT_TURNPOINT]

    @classmethod
    def get_tags(cls) -> list:
        return [cls.TAG_BR, cls.TAG_COMMENT, cls.TAG_HR, cls.TAG_SYMBOL, cls.TAG_TITLE]

    @classmethod
    def get_scene_controls(cls) -> list:
        return [cls.CHANGE_CAMEARA, cls.CHANGE_DATE, cls.CHANGE_STAGE, cls.CHANGE_TIME,
                cls.ELAPSE_DAY, cls.ELAPSE_TIME,
                cls.PUT_OBJECT]
