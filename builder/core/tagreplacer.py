# -*- coding: utf-8 -*-
'''
Tag Replacer Object
===================
'''

from __future__ import annotations

__all__ = ('TagReplacer',)


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
from builder.utils.util_dict import dict_sorted
from builder.utils.util_str import string_replaced_by_tag


# alias
Containable = (Chapter, Episode ,Scene)

# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class TagReplacer(Executer):
    ''' Tag Replacer Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('TAG_REPLACER: initialize')
    #
    # methods
    #

    def execute(self, src: Story, tags: dict) -> ResultData:
        LOG.info('TAG_REPLACER: start exec')
        LOG.debug(f'-- src: {src}')
        LOG.debug(f'-- tags: {tags}')
        is_succeeded = True
        error = None
        tmp = self._exec_internal(src, dict_sorted(tags, True))
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story, tags: dict) -> Story:
        tmp = []
        for child in assertion.is_instance(src, Story).children:
            if isinstance(child, (Chapter, Episode, Scene)):
                tmp.append(self._replaced_in_container(child, tags))
            elif isinstance(child, SCode):
                tmp.append(self._replaced_scode(child, tags))
            else:
                LOG.error(f'Invalid value: {child}')
        return src.inherited(
                *tmp,
                title=string_replaced_by_tag(src.title, tags),
                outline=string_replaced_by_tag(src.outline, tags))

    def _replaced_in_container(self, src: (Chapter, Episode, Scene),
            tags: dict) -> (Chapter, Episode, Scene):
        tmp = []
        if isinstance(src, (Chapter, Episode, Scene)):
            for child in src.children:
                if isinstance(child, (Chapter, Episode, Scene)):
                    tmp.append(self._replaced_in_container(child, tags))
                elif isinstance(child, SCode):
                    tmp.append(self._replaced_scode(child, tags))
                else:
                    LOG.error(f'Invalid replace object!: {type(child)}: {child}')
        else:
            LOG.error(f'Invalid container object!: {type(src)}: {src}')
            return None
        return src.inherited(
                *tmp,
                title=string_replaced_by_tag(src.title, tags),
                outline=string_replaced_by_tag(src.outline, tags),
                )

    def _replaced_scode(self, src: SCode, tags: dict) -> Scode:
        script = assertion.is_instance(src, SCode).script
        def _conv(val, tags):
            if isinstance(val, str):
                return string_replaced_by_tag(val, tags)
            else:
                return val
        if hasattr(src.src, 'calling'):
            script = tuple(_conv(v, dict_sorted(src.src.calling, True)) for v in script)
        script = tuple(_conv(v, tags) for v in script)
        return src.inherited(
                script=script,
                )
