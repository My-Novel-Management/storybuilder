# -*- coding: utf-8 -*-
'''
Comment Converter Object
========================
'''

from __future__ import annotations

__all__ = ('CommentConverter',)


from builder.commands.scode import SCode, SCmd
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


class CommentConverter(Executer):
    ''' Comment Converter Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('CMT_CONVERTER: initialize')
    #
    # methods
    #

    def execute(self, src: Story) -> ResultData:
        LOG.info('CMT_CONVERTER: start exec')
        is_succeeded = True
        error = None
        tmp = assertion.is_instance(self._exec_internal(src), Story)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: ContainerLike) -> (Story, Chapter, Episode, Scene, SCode, None):
        LOG.debug(f'-- src: {src}')
        tmp = []
        if isinstance(src, (Story, Chapter, Episode, Scene, Material)):
            tmp = []
            for child in src.children:
                if isinstance(child, (Chapter, Episode, Scene, Material)):
                    ret = self._exec_internal(child)
                    if ret:
                        tmp.append(ret)
                elif isinstance(child, SCode):
                    tmp.append(child)
                elif isinstance(child, str):
                    tmp.append(SCode(None, SCmd.TAG_COMMENT, (child,), ''))
                else:
                    # NOTE: error check?
                    pass
            return src.inherited(*tmp)
        elif isinstance(src, SCode):
            return src
        else:
            LOG.error()
            return None
