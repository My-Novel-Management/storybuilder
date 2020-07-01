# -*- coding: utf-8 -*-
'''
Filter Object
=============
'''

from __future__ import annotations

__all__ = ('Filter',)


from typing import Tuple, Union
from builder.commands.scode import SCode
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.material import Material
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
ContainerLike = (Story, Chapter, Episode, Scene, SCode, Material)


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class FilterError(BuilderError):
    ''' General Filter Error.
    '''
    pass


class Filter(Executer):
    ''' Filter Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('FILTER: initialize')

    #
    # methods
    #

    def execute(self, src: Story, priority: int) -> ResultData:
        LOG.info('FILTER: start exec')
        tmp, is_succeeded = self._exec_internal(src, priority)
        error = None
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: ContainerLike,
            priority: int) -> Tuple[Union[Story, Chapter, Episode ,Scene, SCode, Material, None], bool]:
        ret = None
        is_succeeded = True
        if isinstance(src, (Story, Chapter, Episode, Scene, Material)):
            if src.priority >= priority:
                tmp = []
                for child in src.children:
                    _, is_succeeded = self._exec_internal(child, priority)
                    if is_succeeded and _:
                        tmp.append(_)
                ret = src.inherited(*tmp)
        elif isinstance(src, SCode):
            if src.priority >= priority:
                ret = src
        else:
            LOG.error(f'Invalid value: {src}')
            is_succeeded = False
        return (ret, is_succeeded)

