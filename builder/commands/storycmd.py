# -*- coding: utf-8 -*-
'''
Story Command Object
====================
'''

from __future__ import annotations

__all__ = ('StoryCmd',)


from typing import Any, Tuple
from builder.commands.command import SCmd
from builder.commands.scode import SCode
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.material import Material
from builder.containers.scene import Scene
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.database import Database
from builder.datatypes.materialtype import MaterialType
from builder.objects.day import Day
from builder.objects.sobject import SObject
from builder.objects.time import Time
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class StoryCmdError(BuilderError):
    ''' General StoryCmd Error.
    '''
    pass


class StoryCmd(object):
    ''' Story Command Object class.
    '''

    def __init__(self, db: Database):
        LOG.info('SCMD: initialize')
        LOG.debug(f'-- db: {db}')
        self._db = assertion.is_instance(db, Database)

    #
    # property
    #

    #
    # method: for Container
    #

    def chapter(self, *args, **kwargs) -> Chapter:
        ''' Create a chapter container and set contents.
        '''
        return Chapter(*args, **kwargs)

    def episode(self, *args, **kwargs) -> Episode:
        ''' Create an episode container and set contents.
        '''
        return Episode(*args, **kwargs)

    def scene(self, *args, **kwargs) -> Scene:
        ''' Create a scene container and set contents.
        '''
        return Scene(*args, **kwargs)

    def document(self, *args, **kwargs) -> Material:
        ''' Create a document container and contents.
        '''
        return Material(MaterialType.DOCUMENT,
                *args, **kwargs)

    def writer_note(self, *args, **kwargs) -> Material:
        ''' Create a writer's note.
        '''
        return Material(MaterialType.WRITER_NOTE,
                *args, **kwargs)

    def character_note(self, *args, **kwargs) -> Material:
        ''' Create a character's note.
        '''
        return Material(MaterialType.CHARACTER_NOTE,
                *args, **kwargs)

    #
    # method: for Plot
    #

    def plot_note(self, *args) -> SCode:
        return SCode(None, SCmd.PLOT_NOTE, args, '')

    def foreshadow(self, *args, flagname: str='') -> SCode:
        return SCode(None, SCmd.PLOT_FORESHADOW, args, flagname)

    def payoff(self, *args, flagname: str='') -> SCode:
        return SCode(None, SCmd.PLOT_PAYOFF, args, flagname)

    def motif(self, motif: str, *args) -> SCode:
        return SCode(None, SCmd.PLOT_MOTIF, args, motif)

    def plot_setup(self, *args, about: str="main") -> SCode:
        return SCode(None, SCmd.PLOT_SETUP, args, about)

    def plot_develop(self, *args, about: str="main") -> SCode:
        return SCode(None, SCmd.PLOT_DEVELOP, args, about)

    def plot_resolve(self, *args, about: str="main") -> SCode:
        return SCode(None, SCmd.PLOT_RESOLVE, args, about)

    def plot_turnpoint(self, *args, about: str="main") -> SCode:
        return SCode(None, SCmd.PLOT_TURNPOINT, args, about)


    #
    # method: for Scene control
    #

    def change_camera(self, key: str) -> SCode:
        return SCode(self._db.get(key), SCmd.CHANGE_CAMEARA, ())

    def change_stage(self, key: str):
        return SCode(self._db.get(key), SCmd.CHANGE_STAGE, ())

    def change_date(self, *args: (int, str)):
        if len(args) > 1 and isinstance(args[0], int):
            tmp = Day('', *args)
            return SCode(tmp, SCmd.CHANGE_DATE, ())
        else:
            return SCode(self._db.get(args[0]), SCmd.CHANGE_DATE, ())

    def change_time(self, *args: (int, str)):
        if len(args) > 1 and isinstance(args[0], int):
            tmp = Time('', *args)
            return SCode(tmp, SCmd.CHANGE_TIME, ())
        else:
            return SCode(self._db.get(args[0]), SCmd.CHANGE_TIME, ())

    def elapse_day(self, month: int=0, day: int=0, year: int=0):
        return SCode(None, SCmd.ELAPSE_DAY, (month, day, year))

    def elapse_time(self, hour: int=0, minute: int=0):
        return SCode(None, SCmd.ELAPSE_TIME, (hour, minute))

    def put(self, *objs: SObject) -> SCode:
        return SCode(None, SCmd.PUT_OBJECT, objs)
