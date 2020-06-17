# -*- coding: utf-8 -*-
'''
Serializer Object
=================
'''

from __future__ import annotations

__all__ = ('Reducer',)


from itertools import chain
from builder.commands.scode import SCode
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
Containable = (Chapter, Episode ,Scene)

# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class SerializerError(BuilderError):
    ''' General Serializer Error.
    '''
    pass


class Serializer(Executer):
    ''' Serializer Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('SERIALIZER: initialize')

    #
    # methods
    #

    def execute(self, src: Story) -> ResultData:
        LOG.info('SERIALIZER: start exec')
        is_succeeded = True
        tmp = CodeList(*self._exec_internal(src))
        error = None
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story) -> list:
        tmp = []
        for child in assertion.is_instance(src, Story).children:
            if isinstance(child, (Chapter, Episode, Scene)):
                tmp.append(self._serialized(child))
            elif isinstance(child, SCode):
                tmp.append([child])
            else:
                LOG.error(f'Invalid story object![1]: {type(child)}: {child}')
        return list(chain.from_iterable(tmp))

    def _serialized(self, src: (Chapter, Episode, Scene)) -> list:
        tmp = []
        for child in assertion.is_various_types(src, (Chapter, Episode, Scene)).children:
            if isinstance(child, (Chapter, Episode)):
                tmp.append(self._serialized(child))
            elif isinstance(child, Scene):
                tmp.append(child.children)
            elif isinstance(child, SCode):
                tmp.append([child])
            else:
                LOG.error(f'Invalid story object![2]: {type(child)}: {child}')
        return list(chain.from_iterable(tmp))
