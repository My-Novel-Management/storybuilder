# -*- coding: utf-8 -*-
'''
Scene Info Updater Object
=========================
'''

from __future__ import annotations

__all__ = ('SceneUpdater',)


from typing import Tuple
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.material import Material
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.resultdata import ResultData
from builder.datatypes.sceneinfo import SceneInfo
from builder.objects.day import Day
from builder.objects.person import Person
from builder.objects.stage import Stage
from builder.objects.time import Time
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
ContainerLike = (Story, Chapter, Episode, Scene, SCode, Material)


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class SceneUpdaterError(BuilderError):
    ''' General Error of SceneUpdater.
    '''
    pass


class SceneUpdater(Executer):
    ''' Scene Updater Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('SCENE_UPDATER: initialize')

    #
    # methods
    #

    def execute(self, src: Story) -> ResultData:
        LOG.info('SCENE_UPDATER: start exec')
        tmp, is_succeeded, error = assertion.is_tuple(self._exec_internal(src))
        return ResultData(
                assertion.is_instance(tmp, Story),
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story) -> Tuple[Story, bool, (SceneUpdaterError, None)]:
        assertion.is_instance(src, Story)

        tmp = []
        is_succeeded = True
        error = None
        camera = None
        stage = None
        day = None
        time = None

        for child in src.children:
            if isinstance(child, (Chapter, Episode, Scene)):
                LOG.debug(f'>> {camera.name if camera else camera}/{stage.name if stage else stage}/{day.name if day else day}/{time.name if time else time}')
                ret, camera, stage, day, time = self._updated_scene_info(child, camera, stage, day, time)
                tmp.append(ret)
            elif isinstance(child, SCode):
                tmp.append(child)
            elif isinstance(child, Material):
                tmp.append(child)
            else:
                msg = f'Invalid a child value in scene_update_exec!: {type(child)}: {child}'
                LOG.error(msg)
                error = SceneUpdaterError(msg)
        return src.inherited(*tmp), is_succeeded, error


    def _updated_scene_info(self, src: (Chapter, Episode, Scene, SCode),
            camera: Person=None,
            stage: Stage=None,
            day: Day=None,
            time: Time=None) -> Tuple[(Chapter, Episode, Scene), (Person, None), (Stage, None), (Day, None), (Time, None)]:
        if isinstance(src, (Chapter, Episode)):
            tmp = []
            for child in src.children:
                ret, camera, stage, day, time = self._updated_scene_info(child, camera, stage, day, time)
                tmp.append(ret)
            return src.inherited(*tmp), camera, stage, day, time
        elif isinstance(src, Scene):
            ret = self._get_scene_info(src)
            if not ret:
                LOG.error(f'Not found a SceneInfo!: in {src.title} scene')
                return src, camera, stage, day, time
            else:
                assertion.is_instance(ret, SCode)
                info = assertion.is_instance(ret.script[0], SceneInfo)
                camera = info.camera if info.camera else camera
                stage = info.stage if info.stage else stage
                day = info.day if info.day else day
                time = info.time if info.time else time
                codes = []
                for child in src.children:
                    if self._is_scene_info(child):
                        codes.append(child.inherited(script=(SceneInfo(camera, stage, day, time),)))
                    else:
                        codes.append(child)
            return src.inherited(*codes), camera, stage, day, time
        elif isinstance(src, SCode):
            return src, camera, stage, day, time
        else:
            LOG.error(f'Invalid value in updated_scene_info: {src}')
            return src, camera, stage, day, time

    def _get_scene_info(self, src: Scene) -> (SCode, None):
        for child in assertion.is_instance(src, Scene).children:
            if self._is_scene_info(child):
                return child
        return None

    def _is_scene_info(self, src) -> bool:
        return isinstance(src, SCode) and src.cmd is SCmd.INFO_DATA and isinstance(src.script[0], SceneInfo)
