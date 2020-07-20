# -*- coding: utf-8 -*-
'''
Plot Info Updater Object
========================
'''

from __future__ import annotations

__all__ = ('PlotUpdater',)


from itertools import chain
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
from builder.datatypes.plotinfo import PlotInfo
from builder.utils import assertion
from builder.utils import util_list
from builder.utils.logger import MyLogger


# alias
ContainerLike = (Story, Chapter, Episode, Scene, SCode, Material)


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class PlotUpdaterError(BuilderError):
    ''' General Error of PlotUpdater.
    '''
    pass


class PlotUpdater(Executer):
    ''' Plot Updater Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('PLOT_UPDATER: initialize')

    #
    # methods
    #

    def execute(self, src: Story) -> ResultData:
        LOG.info('PLOT_UPDATER: start exec')
        tmp, is_succeeded, error = assertion.is_tuple(self._exec_internal(src))
        return ResultData(
                assertion.is_instance(tmp, Story),
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story) -> Tuple[Story, bool, (PlotUpdaterError, None)]:
        assertion.is_instance(src, Story)

        tmp = []
        is_succeeded = True
        error = None

        titles = self._collect_plot_title(src)

        infos = []
        for title in titles:
            ret = self._updated_plot_info(src, title)
            if ret:
                infos.append(PlotInfo(title, *ret))

        ret = self._inserted_after_storyinfo(src, infos)
        return ret, is_succeeded, error


    def _collect_plot_title(self, src: ContainerLike) -> list:
        tmp = []
        for child in src.children:
            if isinstance(child, (Chapter, Episode, Scene, Material)):
                tmp.extend(self._collect_plot_title(child))
            elif isinstance(child, SCode):
                if child.cmd in SCmd.get_plot_structs():
                    tmp.append(child.option)
        return list(set(tmp))

    def _updated_plot_info(self, src: Story, title: str) -> list:
        assertion.is_instance(src, Story)
        tmp = []
        for child in src.children:
            ret = self._updated_plot_info_internal(child, title)
            if ret:
                tmp.extend(ret)
        return tmp

    def _updated_plot_info_internal(self, src: (Chapter, Episode, Scene, Material, SCode),
            title: str) -> list:
        if isinstance(src, (Chapter, Episode, Scene, Material)):
            tmp = []
            for child in src.children:
                ret = self._updated_plot_info_internal(child, title)
                if ret:
                    tmp.extend(ret)
            return tmp
        elif isinstance(src, SCode):
            if src.cmd in SCmd.get_plot_structs() and src.option == title:
                return [src]
        else:
            LOG.error('Invalid value in updated_plot_info_internal: {src}')
            return []

    def _inserted_after_storyinfo(self, src: Story, infos: list) -> Story:
        assertion.is_instance(src, Story)
        LOG.debug(f'- info in inserted_after_storyinfo:{infos}')

        tmp = []
        for child in src.children:
            if isinstance(child, SCode) and child.cmd is SCmd.INFO_STORY:
                tmp.append(child)
                for info in infos:
                    tmp.append(SCode(None, SCmd.INFO_DATA, (info,), ""))
            else:
                tmp.append(child)
        return src.inherited(*tmp)

