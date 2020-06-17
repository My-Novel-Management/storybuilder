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
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
Containable = (Chapter, Episode, Scene)

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
        is_succeeded = True
        tmp = []
        error = None
        for child in assertion.is_instance(src, Story).children:
            ret, is_succeeded = self._exec_internal(child, priority)
            if is_succeeded and ret:
                tmp.append(assertion.is_instance(ret,
                    (Chapter, Episode, Scene, SCode)))
            elif not is_succeeded:
                error = FilterError('Invalid value in Filter!')
                break
        return ResultData(
                src.inherited(*tmp),
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: (Chapter, Episode, Scene, SCode),
            priority: int) -> Tuple[Union[Chapter, Episode ,Scene, SCode, None], bool]:
        tmp = []
        is_succeeded = True
        if isinstance(src, (Chapter, Episode, Scene)):
            for child in src.children:
                if child.priority >= priority:
                    ret, is_succeeded = self._exec_internal(child, priority)
                    if is_succeeded and ret:
                        tmp.append(ret)
            return src.inherited(*tmp), is_succeeded
        elif isinstance(src, SCode):
            return (src, is_succeeded) if src.priority >= priority else (None, is_succeeded)
        else:
            LOG.error(f'Invalid value: {src}')
            is_succeeded = False
            return (None, is_succeeded)

