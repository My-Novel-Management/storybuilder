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
from builder.containers.material import Material
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.compilemode import CompileMode
from builder.datatypes.resultdata import ResultData
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
ContainerLike = (Story, Chapter, Episode, Scene, SCode, Material)


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

    def execute(self, src: Story, mode: CompileMode) -> ResultData:
        LOG.info('SERIALIZER: start exec')
        is_succeeded = True
        tmp = CodeList(*self._exec_internal(src, mode))
        error = None
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story, mode: CompileMode) -> list:
        ret = []
        assertion.is_instance(src, Story)
        if assertion.is_instance(mode, CompileMode) in (CompileMode.NORMAL, CompileMode.NOVEL_TEXT):
            ret = self._novel_serialized(src)
        elif mode is CompileMode.PLOT:
            ret = self._plot_serialized(src)
        elif mode is CompileMode.STORY_DATA:
            ret = self._storydata_serialized(src)
        elif mode is CompileMode.SCENARIO:
            ret = []
        elif mode is CompileMode.AUDIODRAMA:
            ret = []
        else:
            LOG.error(f'Invalid story object![1]: {type(child)}: {child}')
        return ret

    def _novel_serialized(self, src: ContainerLike) -> list:
        ''' NOTE: omit Material parts.
        '''
        if isinstance(src, (Story, Chapter, Episode, Scene)):
            tmp = []
            for child in assertion.is_various_types(src, (Story, Chapter, Episode, Scene, Material)).children:
                if isinstance(child, (Story, Chapter, Episode)):
                    tmp.append(self._novel_serialized(child))
                elif isinstance(child, Scene):
                    tmp.append(child.children)
                elif isinstance(child, SCode):
                    tmp.append([child])
                elif isinstance(child, Material):
                    continue
                else:
                    LOG.error(f'Invalid story object![3]: {type(child)}: {child}')
            return list(chain.from_iterable(tmp))
        elif isinstance(src, SCode):
            return [src]
        elif isinstance(src, Material):
            return []
        else:
            LOG.error(f'Invalid story object![2]: {type(src)}: {src}')
            return []

    def _plot_serialized(self, src: ContainerLike) -> list:
        if isinstance(src, (Story, Chapter, Episode, Scene, Material)):
            tmp = []
            for child in src.children:
                if isinstance(child, (Story, Chapter, Episode)):
                    tmp.append(self._plot_serialized(child))
                elif isinstance(child, Scene):
                    tmp.append(child.children)
                elif isinstance(child, SCode):
                    tmp.append([child])
                elif isinstance(child, Material):
                    tmp.append(child.children)
                else:
                    LOG.error(f'Invalid story object![4]: {type(child)}: {child}')
            return list(chain.from_iterable(tmp))
        elif isinstance(src, SCode):
            return [src]
        else:
            LOG.error(f'Invalid story object![5]: {type(src)}: {src}')
            return []

    def _storydata_serialized(self, src: ContainerLike) -> list:
        if isinstance(src, (Story, Chapter, Episode, Scene, Material)):
            tmp = []
            for child in src.children:
                if isinstance(child, Material):
                    tmp.append(child.children)
                elif isinstance(child, (Story, Chapter, Episode, Scene)):
                    continue
                elif isinstance(child, SCode):
                    tmp.append([child])
                else:
                    LOG.error(f'Invalid story object![6]: {type(child)}: {child}')
            return list(chain.from_iterable(tmp))
        elif isinstance(src, SCode):
            return [src]
        else:
            LOG.error(f'Invalid story object![7]: {type(child)}: {child}')
            return []

