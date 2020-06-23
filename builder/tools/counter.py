# -*- coding: utf-8 -*-
'''
Counter Object
==============
'''

from __future__ import annotations

__all__ = ('Counter',)


from typing import Any
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.tools.checker import Checker
from builder.tools.converter import Converter
from builder.utils import assertion
from builder.utils.logger import MyLogger
from builder.utils.util_math import int_ceil


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Counter(object):
    ''' Counter Object class.
    '''

    #
    # methods (container numbers)
    #

    def chapters_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        if isinstance(src, Story):
            return len([child for child in src.children if isinstance(child, Chapter)])
        elif isinstance(src, Chapter):
            return 1
        elif isinstance(src, (Episode, Scene, SCode)):
            return 0
        elif isinstance(src, (list, tuple)):
            return sum([self.chapters_of(child) for child in src])
        else:
            LOG.error(f'Invalid source in chapters_of: {type(src)}: {src}')
            return 0

    def episodes_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        if isinstance(src, Story):
            return sum([self.episodes_of(child) for child in src.children])
        elif isinstance(src, Chapter):
            return len([child for child in src.children if isinstance(child, Episode)])
        elif isinstance(src, Episode):
            return 1
        elif isinstance(src, (Scene, SCode)):
            return 0
        elif isinstance(src, (list, tuple)):
            return sum([self.episodes_of(child) for child in src])
        else:
            LOG.error(f'Invalid source in episodes_of: {type(src)}: {src}')
            return 0

    def scenes_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        if isinstance(src, (Story, Chapter)):
            return sum([self.scenes_of(child) for child in src.children])
        elif isinstance(src, Episode):
            return len([child for child in src.children if isinstance(child, Scene)])
        elif isinstance(src, Scene):
            return 1
        elif isinstance(src, SCode):
            return 0
        elif isinstance(src, (list, tuple)):
            return sum([self.scenes_of(child) for child in src])
        else:
            LOG.error(f'Invalid source in scenes_of: {type(src)}: {src}')
            return 0

    def scodes_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        if isinstance(src, (Story, Chapter, Episode)):
            return sum([self.scodes_of(child) for child in src.children])
        elif isinstance(src, Scene):
            return len([child for child in src.children if isinstance(child, SCode)])
        elif isinstance(src, SCode):
            return 1
        elif isinstance(src, (list, tuple)):
            return sum([self.scodes_of(child) for child in src])
        else:
            LOG.error(f'Invalid source in scodes_of: {type(src)}: {src}')
            return 0

    def scodes_of_without_info(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        def _validate_scode(val: SCode):
            return not val.cmd in SCmd.get_informations()
        if isinstance(src, (Story, Chapter, Episode)):
            return sum([self.scodes_of_without_info(child) for child in src.children])
        elif isinstance(src, Scene):
            return len([child for child in src.children if isinstance(child, SCode) and _validate_scode(child)])
        elif isinstance(src, SCode):
            return 1 if _validate_scode(src) else 0
        elif isinstance(src, (list, tuple)):
            return sum([self.scodes_of_without_info(child) for child in src])
        else:
            LOG.error(f'Invalid source in scodes_of_without_info: {type(src)}: {src}')
            return 0

    #
    # methods (character numbers)
    #

    def description_characters_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        def _validate_scode(val: SCode):
            return val.cmd in SCmd.get_all_actions()
        def _correct(val: SCode):
            if val.cmd in SCmd.get_dialogue_actions():
                return 2
            elif val.cmd in SCmd.get_normal_actions():
                return 1
            else:
                return 0
        if isinstance(src, (Story, Chapter, Episode, Scene)):
            return sum([self.description_characters_of(child) for child in src.children])
        elif isinstance(src, SCode):
            conv = Converter()
            if _validate_scode(src):
                tmp = len("。".join(conv.script_relieved_symbols(src.script)))
                return tmp + _correct(src) if tmp else tmp
            else:
                return 0
        elif isinstance(src, (list, tuple)):
            return sum([self.description_characters_of(child) for child in src])
        else:
            LOG.error(f'Invalid source in description_characters_of: {type(src)}: {src}')
            return 0

    def total_characters_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple)) -> int:
        if isinstance(src, (Story, Chapter, Episode, Scene)):
            return sum([self.total_characters_of(child) for child in src.children])
        elif isinstance(src, SCode):
            return len("。".join(Converter().script_relieved_strings(src.script)))
        elif isinstance(src, (list, tuple)):
            return sum([self.total_characters_of(child) for child in src])
        else:
            LOG.error(f'Invalid source in total_characters_of: {type(src)}: {src}')

    #
    # methods (manupapers)
    #

    def manupaper_numbers_of(self, lines: int, rows: int) -> float:
        ''' Count manupaper numbers, using manupaper line numbers.
        '''
        return lines / rows if rows else 0

    def manupaper_rows_of(self, src: (Story, Chapter, Episode, Scene, SCode, list, tuple),
            columns: int) -> int:
        if isinstance(src, (Story, Chapter, Episode)):
            return sum(self.manupaper_rows_of(child, columns) for child in src.children)
        elif isinstance(src, Scene):
            checker = Checker()
            ret = []
            tmp = 0
            for child in src.children:
                if assertion.is_instance(child, SCode).cmd in SCmd.get_all_actions():
                    if checker.is_empty_script(child):
                        if tmp:
                            ret.append(int_ceil(tmp, columns))
                            tmp = 0
                            continue
                        else:
                            continue
                    tmp += self.description_characters_of(child)
                elif child.cmd in SCmd.get_end_of_containers():
                    continue
                elif child.cmd in SCmd.get_informations():
                    continue
                elif child.cmd in SCmd.get_scene_controls():
                    continue
                elif child.cmd in SCmd.get_tags():
                    if child.cmd is SCmd.TAG_BR:
                        tmp = 1
                    elif child.cmd is SCmd.TAG_SYMBOL:
                        tmp = 2
                    else:
                        tmp = 0
                if not checker.has_then(child):
                    ret.append(int_ceil(tmp, columns))
                    tmp = 0
            if tmp:
                ret.append(int_ceil(tmp, columns))
            return sum(ret)
        elif isinstance(src, SCode):
            # actions
            if assertion.is_instance(src, SCode).cmd in SCmd.get_all_actions():
                return int_ceil(self.description_characters_of(src) + 2, columns)
            # then
            elif code.cmd is SCmd.THEN:
                pass
            # container break
            elif code.cmd in SCmd.end_of_containers():
                pass
            # tag
            elif code.cmd in SCmd.tags():
                if code.cmd is SCmd.TAG_BR:
                    return 1
                elif code.cmd is SCmd.TAG_SYMBOL:
                    return 2
                else:
                    return 0
            # info
            elif code.cmd in SCmd.informations():
                pass
            # scene control
            elif code.cmd in SCmd.scene_controls():
                pass
            else:
                msg = f'Invalid SCmd: {code.cmd}'
                LOG.critical(msg)
            return 0
        elif isinstance(src, (list, tuple)):
            return sum(self.manupaper_rows_of(child, columns) for child in src)
        else:
            msg = 'Error'
            LOG.critical(msg)
            return 0

