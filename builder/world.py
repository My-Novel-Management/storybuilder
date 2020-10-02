# -*- coding: utf-8 -*-
'''
Story World  Object
===================
'''

from __future__ import annotations

__all__ = ('World',)


from builder import VERSION_MSG, __DEFAULT_LOG_LEVEL__, __VERSION__, __TITLE__
from builder.commands.optioncmd import OptionParser
from builder.commands.scode import SCode, SCmd
from builder.commands.storycmd import StoryCmd
from builder.commands.tagcmd import TagCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.runner import Runner
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.database import Database
from builder.datatypes.resultdata import ResultData
from builder.datatypes.storyconfig import StoryConfig
from builder.objects.sobject import SObject
from builder.utils import assertion
from builder.utils.util_date import get_date_lastmodified
from builder.utils.util_file import get_module_filename
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Writer(object):
    ''' Writer Object class.
    '''

    def __init__(self, src: SObject):
        self._src = assertion.is_instance(src, SObject)

    #
    # methods
    #

    def be(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.BE, args)

    def come(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.COME, args)

    def do(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.DO, args)

    def explain(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.EXPLAIN, args)

    def go(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.GO, args)

    def hear(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.HEAR, args)

    def look(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.LOOK, args)

    def talk(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.TALK, args)

    def think(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.THINK, args)

    def voice(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.VOICE, args)

    def wear(self, *args: str) -> SCode:
        return SCode(self._src, SCmd.WEAR, args)


class World(object):
    ''' Story World Object class.
    '''

    def __init__(self, title: str, loglevel: str=__DEFAULT_LOG_LEVEL__):
        # log
        LOG.set_level(loglevel)
        # start logging
        LOG.info('--------' * 4 + f' START LOGGING [{LOG.level}]' + '--------' * 4)
        LOG.info('CLASS: World: initialize')
        LOG.debug(f'-- title: {title}')
        # data
        self._config = StoryConfig(title)
        self._db = Database()
        # command
        self._cmd = StoryCmd(self._db)
        self._tag = TagCmd()
        # hook method
        self.chapter = self._cmd.chapter
        self.episode = self._cmd.episode
        self.scene = self._cmd.scene
        self.plot_note = self._cmd.plot_note
        self.foreshadow = self._cmd.foreshadow
        self.payoff = self._cmd.payoff
        self.motif = self._cmd.motif
        self.plot_setup = self._cmd.plot_setup
        self.plot_develop = self._cmd.plot_develop
        self.plot_resolve = self._cmd.plot_resolve
        self.plot_turnpoint = self._cmd.plot_turnpoint
        self.writer_note = self._cmd.writer_note
        self.chara_note = self._cmd.character_note
        self.document = self._cmd.document
        self.br = self._tag.br
        self.comment = self._tag.comment
        self.symbol = self._tag.symbol
        self._config.set_log_level(loglevel)
        self.change_camera = self.cmd.change_camera
        self.change_stage = self.cmd.change_stage
        self.change_date = self.cmd.change_date
        self.change_time = self.cmd.change_time

    #
    # static methods
    #

    @staticmethod
    def create_world(title: str) -> World: # pragma: no cover
        ''' Get world class instance.
        '''
        # first print
        print(f'>> Build by {__TITLE__}(v{__VERSION__})')
        # log level set
        LOG.reset_logger(OptionParser().get_commandline_arguments())
        tmp = World(title)
        # default settings
        tmp.config.set_modified(get_date_lastmodified(get_module_filename(2)))
        return tmp

    #
    # property
    #

    @property
    def config(self) -> StoryConfig:
        return self._config

    @property
    def db(self) -> Database:
        return self._db

    @property
    def cmd(self) -> StoryCmd:
        return self._cmd

    @property
    def tag(self) -> TagCmd:
        return self._tag

    #
    # methods
    #

    def get(self, key: str) -> Writer:
        return Writer(self._db.get(key))


    def run(self, *args: (Chapter, Episode, Scene, SCode)) -> int: # pragma: no cover
        ''' Run the story builder.
        '''
        LOG.info('WORLD: START: run')
        exit_msg = ''
        exit_code = 0
        try:
            LOG.info('WORLD: create story object')
            # TODO: validate args
            tmp = Story(self.config.title, *args, outline=self.config.outline)
            LOG.info('WORLD: START: runner')
            result = assertion.is_instance(
                        Runner().execute(tmp, self.config, self.db),
                        ResultData)
            if not result.is_succeeded:
                if result.error:
                    raise result.error
                else:
                    raise BuilderError('Other Builder Error!!')
            LOG.info('... SUCCESS: runner')
        except Exception as e:
            import traceback
            ex_traceback = traceback.format_exc()
            exit_msg += '==== BUILDER ERROR ====\n' + '\n'.join(VERSION_MSG)
            exit_msg += f'\n: {ex_traceback}'
            exit_code = 1
        except SystemExit as ex:
            if ex.code is not None:
                if not isinstance(ex.code, int):
                    exit_msg = ex_code
                    exit_code = 1
                else:
                    exit_code = ex.code
        finally:
            import sys
            if exit_msg:
                LOG.critical(exit_msg)
            if exit_msg:
                sys.stderr.write(exit_msg)
            return exit_code

