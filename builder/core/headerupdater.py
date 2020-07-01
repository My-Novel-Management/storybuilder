# -*- coding: utf-8 -*-
'''
Header Updater Object
=====================
'''

from __future__ import annotations

__all__ = ('HeaderUpdater',)


from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.material import Material
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.headerinfo import HeaderInfo
from builder.datatypes.resultdata import ResultData
from builder.datatypes.storyconfig import StoryConfig
from builder.tools.checker import Checker
from builder.tools.collecter import Collecter
from builder.tools.counter import Counter
from builder.utils import assertion
from builder.utils.logger import MyLogger


# alias
StoryObjectLike = (Story, Chapter, Episode ,Scene, SCode, Material)


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class HeaderUpdater(Executer):
    ''' Header Updater Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('HEAD_UPDATE: intialize')

    #
    # methods
    #

    def execute(self, src: Story, config: StoryConfig) -> ResultData:
        LOG.info('HEAD_UPDATE: start exec')
        is_succeeded = True
        error = None
        tmp = assertion.is_instance(self._exec_internal(src, config),
                Story)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods
    #

    def _exec_internal(self, src: Story, config: StoryConfig) -> Story:
        tmp = []
        columns = config.columns
        rows = config.rows
        assertion.is_instance(src, Story)

        tmp.append(self._collect_header_info(src, columns, rows))
        tmp.append(self._title_of(src))
        if src.outline:
            tmp.append(self._outline_of(src))
        tmp.append(self._get_contents(src))

        for child in src.children:
            if isinstance(child, (Chapter, Episode, Scene)):
                tmp.append(self._update_container_info(child, columns, rows))
            elif isinstance(child, SCode):
                tmp.append(child)
            elif isinstance(child, Material):
                tmp.append(self._update_container_info(child, columns, rows))
            else:
                LOG.error(f'Invalid a child value!: {type(child)}: {child}')
        tmp.append(self._get_story_info(src, config))

        return src.inherited(*tmp)


    def _update_container_info(self, src: (Chapter, Episode, Scene, Material),
            columns: int, rows: int) -> (Chapter, Episode, Scene, Material):
        LOG.info('HEAD_UPDATER: update_container_info')
        LOG.debug(f'-- src: {src}')
        LOG.debug(f'-- columns/rows: {columns}/{rows}')

        assertion.is_instance(src, (Chapter, Episode, Scene, Material))

        tmp = []
        tmp.append(self._collect_header_info(src, columns, rows))
        tmp.append(self._title_of(src))
        if src.outline:
            tmp.append(self._outline_of(src))
        for child in src.children:
            if isinstance(child, (Chapter, Episode, Scene)):
                tmp.append(self._update_container_info(child, columns, rows))
            elif isinstance(child, SCode):
                if Checker().has_then(child):
                    tmp.append(SCode(None, SCmd.THEN, (), ''))
                tmp.append(child)
            elif isinstance(child, Material):
                tmp.append(self._update_container_info(child, columsn, rows))
            else:
                LOG.error(f'Invalid child value!: {type(child)} | {child}')
        tmp.append(self._end_of(src))
        return src.inherited(*tmp)

    def _collect_header_info(self, src: (Story, Chapter, Episode, Scene, Material),
            columns: int, rows: int) -> SCode:
        count = Counter()
        total_lines = count.manupaper_rows_of(src, columns, True)
        lines = count.manupaper_rows_of(src, columns)
        return SCode(None, SCmd.INFO_DATA,
                (HeaderInfo(
                    count.total_characters_of(src),
                    total_lines,
                    count.manupaper_numbers_of(total_lines, rows),
                    count.description_characters_of(src),
                    lines,
                    count.manupaper_numbers_of(lines, rows),
                    count.chapters_of(src),
                    count.episodes_of(src),
                    count.scenes_of(src),
                    count.scodes_of_without_info(src),
                    ),),
                '')

    def _title_of(self, src: (Story, Chapter, Episode, Scene, Material)) -> SCode:
        level = 0
        if isinstance(src, Story):
            level = 1
        elif isinstance(src, Chapter):
            level = 2
        elif isinstance(src, Episode):
            level = 3
        elif isinstance(src, Scene):
            level = 4
        elif isinstance(src, Material):
            level = 2
        else:
            LOG.critical(f'Invalid source of a story object: {type(src)}: {src}')
        return SCode(None, SCmd.TAG_TITLE, (src.title,), level)

    def _outline_of(self, src: (Story, Chapter, Episode, Scene, Material)) -> SCode:
        return SCode(None, SCmd.TAG_COMMENT, (src.outline,), "outline")

    def _end_of(self, src: (Chapter, Episode, Scene, Material)) -> (SCode, None):
        if isinstance(src, Chapter):
            return SCode(None, SCmd.END_CHAPTER, (), '')
        elif isinstance(src, Episode):
            return SCode(None, SCmd.END_EPISODE, (), '')
        elif isinstance(src, Scene):
            return SCode(None, SCmd.END_SCENE, (), '')
        elif isinstance(src, Material):
            return SCode(None, SCmd.END_MATERIAL, (), '')
        else:
            LOG.error(f'Invalid source!: {src}')
            return None

    def _get_contents(self, src: Story) -> SCode:
        collect = Collecter()
        tmp = []
        ch_n = ep_n = sc_n = 1
        titles = collect.container_titles(src)
        for title_set in titles:
            level, title = title_set.split(':')
            if level == '0':
                continue
            elif level == '1':
                tmp.append(f'{ch_n}. {title}')
                ch_n += 1
            elif level == '2':
                tmp.append(f'    {ep_n}. {title}')
                ep_n += 1
            elif level == '3':
                tmp.append(f'        {sc_n}. {title}')
                sc_n += 1
            else:
                continue
        return SCode(None, SCmd.TAG_TITLE, ('\n'.join(tmp),), 'contents')

    def _get_story_info(self, src: Story, config: StoryConfig) -> SCode:
        version = config.version
        return SCode(None, SCmd.INFO_CONTENT, (f'version: {version}',), '')
