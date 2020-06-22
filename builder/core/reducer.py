# -*- coding: utf-8 -*-
'''
Reducer Object
==============
'''

from __future__ import annotations

__all__ = ('Reducer',)


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
Containable = (Chapter, Episode ,Scene)

# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Reducer(Executer):
    ''' Reducer Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('REDUCER: initialize')
    #
    # methods
    #

    def execute(self, src: Story, start: int, end: int) -> ResultData:
        LOG.info('REDUCER: start exec')
        is_succeeded = True
        error = None
        tmp = assertion.is_instance(self._exec_internal(src, start, end),
                Story)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story, start: int, end: int) -> Story:
        LOG.debug(f'-- src: {src}')
        LOG.debug(f'-- start/end: {start}/{end}')
        assertion.is_int(start)
        assertion.is_int(end)
        tmp = []
        idx = 0
        # TODO: start and end check
        for child in assertion.is_instance(src, Story).children:
            if isinstance(child, (Chapter, Episode)):
                if idx >= start and (idx <= end or end < 0):
                    tmp.append(child)
                idx += 1
            else:
                tmp.append(child)
        return src.inherited(*tmp)
