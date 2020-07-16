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
from builder.containers.material import Material
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.resultdata import ResultData
from builder.datatypes.storyconfig import StoryConfig
from builder.utils import assertion
from builder.utils.logger import MyLogger
from builder.utils.util_dict import dict_sorted, combine_dict
from builder.utils.util_str import string_replaced_by_tag


# alias
ContainerLike = (Story, Chapter, Episode, Scene, SCode, Material)


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

    def execute(self, src: Story, config: StoryConfig, tags: dict) -> ResultData:
        LOG.info('TAG_REPLACER: start exec')
        LOG.debug(f'-- src: {src}')
        LOG.debug(f'-- config: {config}')
        LOG.debug(f'-- tags: {tags}')
        is_succeeded = True
        error = None
        tmp = self._exec_internal(src, dict_sorted(tags, True))
        is_succeeded = self._config_data_replaced(config, dict_sorted(tags, True))
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
            if isinstance(child, (Chapter, Episode, Scene, Material)):
                tmp.append(self._replaced_in_container(child, tags))
            elif isinstance(child, SCode):
                tmp.append(self._replaced_scode(child, tags))
            else:
                LOG.error(f'Invalid value: {child}')
        return src.inherited(
                *tmp,
                title=string_replaced_by_tag(src.title, tags),
                outline=string_replaced_by_tag(src.outline, tags))


    def _config_data_replaced(self, config: StoryConfig, tags: dict) -> bool:
        assertion.is_instance(config, StoryConfig)

        is_succeeded = True

        config.set_title(string_replaced_by_tag(config.title, tags))
        config.set_copy(string_replaced_by_tag(config.copy, tags))
        config.set_oneline(string_replaced_by_tag(config.oneline, tags))
        config.set_outline(string_replaced_by_tag(config.outline, tags))

        return is_succeeded


    def _replaced_in_container(self, src: (Chapter, Episode, Scene, Material),
            tags: dict) -> (Chapter, Episode, Scene):
        tmp = []
        if isinstance(src, (Chapter, Episode, Scene, Material)):
            for child in src.children:
                if isinstance(child, (Chapter, Episode, Scene, Material)):
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
        _tags = tags
        def _conv(val, tags):
            if isinstance(val, str):
                return string_replaced_by_tag(val, tags)
            else:
                return val
        if hasattr(src.src, 'calling'):
            _tags = dict_sorted(combine_dict(tags, src.src.calling), True)
        script = tuple(_conv(v, _tags) for v in script)
        return src.inherited(
                script=script,
                )
