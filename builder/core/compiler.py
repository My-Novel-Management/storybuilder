# -*- coding: utf-8 -*-
'''
Compiler Object
===============
'''

from __future__ import annotations

__all__ = ('Compiler',)


from enum import Enum, auto
from typing import Tuple
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.core.executer import Executer
from builder.datatypes.builderexception import BuilderError
from builder.datatypes.codelist import CodeList
from builder.datatypes.compilemode import CompileMode
from builder.datatypes.formattag import FormatTag
from builder.datatypes.headerinfo import HeaderInfo
from builder.datatypes.rawdata import RawData
from builder.datatypes.resultdata import ResultData
from builder.objects.rubi import Rubi
from builder.tools.checker import Checker
from builder.tools.converter import Converter
from builder.utils import assertion
from builder.utils.logger import MyLogger
from builder.utils.util_str import validate_string_duplicate_chopped, validate_dialogue_brackets


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class CompileModeError(BuilderError):
    ''' Exception of Compile mode mismatch.
    '''
    pass


class CompileSCmdError(BuilderError):
    ''' Exception of Compile SCode command mismatch.
    '''
    pass


class Compiler(Executer):
    ''' Compiler Executer class.
    '''
    def __init__(self):
        super().__init__()
        LOG.info('COMPILER: initialize')

    #
    # methods
    #

    def execute(self, src: CodeList, mode: CompileMode,
            rubis: dict=None, is_rubi: bool=False, is_comment: bool=True) -> ResultData:
        LOG.info('COMPILER: start exec')

        is_succeeded = True
        tmp = []
        error = None

        if assertion.is_instance(mode, CompileMode) is CompileMode.NORMAL:
            tmp = assertion.is_instance(self._conv_to_novel(src, is_comment), RawData)
            if is_rubi:
                tmp = assertion.is_instance(self._add_rubi_on_novel(tmp, rubis),
                        RawData)
        elif mode is CompileMode.PLOT:
            tmp = assertion.is_instance(self._conv_to_plot(src), RawData)
        elif mode is CompileMode.NOVEL_TEXT:
            tmp = assertion.is_instance(self._conv_to_novel(src, is_comment), RawData)
            tmp = assertion.is_instance(self._conv_to_text(tmp), RawData)
            if is_rubi:
                tmp = assertion.is_instance(self._add_rubi_on_novel(tmp, rubis), RawData)
        elif mode is CompileMode.SCENARIO:
            tmp = src
        elif mode is CompileMode.AUDIODRAMA:
            tmp = src
        else:
            msg = f'Invalid CompileMode!: {mode}'
            LOG.error(msg)
            error = CompileModeError(msg)
        return ResultData(
                tmp,
                is_succeeded,
                error)

    #
    # private methods (novel)
    #

    def _conv_to_novel(self, src: CodeList, is_comment: bool) -> RawData:
        LOG.info('COMP: conv_to_novel start')

        tmp = []
        checker = Checker()
        conv = Converter()
        is_added = False
        is_then = False
        in_dialogue = False
        desc_head = "　"
        head_info = ""
        dial_stock = None
        ch_num = ep_num = sc_num = 1

        for code in assertion.is_instance(src, CodeList).data:
            assertion.is_instance(code, SCode)
            # actions
            if code.cmd in SCmd.get_normal_actions():
                if not checker.is_empty_script(code):
                    if not is_then:
                        tmp.append(FormatTag.DESCRIPTION_HEAD)
                    tmp.append(f'{desc_head}{conv.to_description(conv.script_relieved_symbols(code.script))}')
                    is_added = True
            elif code.cmd in SCmd.get_dialogue_actions():
                is_voice = code.cmd is SCmd.VOICE
                script = conv.script_relieved_symbols(code.script)
                if dial_stock:
                    script = dial_stock + script
                    dial_stock = None
                if not is_then:
                    tmp.append(FormatTag.DIALOGUE_HEAD)
                    if is_voice:
                        tmp.append(f'{conv.to_dialogue(script, ("『", "』"))}')
                    else:
                        tmp.append(f'{conv.to_dialogue(script)}')
                else:
                    dial_stock = conv.script_relieved_symbols(code.script)
                is_added = True
            # then
            elif code.cmd is SCmd.THEN:
                is_then = True
            # container break
            elif code.cmd in SCmd.get_end_of_containers():
                tmp.append(self._conv_from_end_container(code))
            # tag
            elif code.cmd in SCmd.get_tags():
                ret, (ch_num, ep_num, sc_num) = self._conv_from_tag(code, head_info,
                        (ch_num, ep_num, sc_num), is_comment)
                if ret:
                    tmp.append(FormatTag.SYMBOL_HEAD if code.cmd is SCmd.TAG_SYMBOL else FormatTag.TAG_HEAD)
                    tmp.append(ret)
            # info
            elif code.cmd in SCmd.get_informations():
                if code.cmd is SCmd.INFO_DATA:
                    head_info = self._get_headinfo(code)
                elif code.cmd is SCmd.INFO_CONTENT:
                    tmp.append(self._get_storyinfo(code))
                continue
            # scene control
            elif code.cmd in SCmd.get_scene_controls():
                continue
            # plot control
            elif code.cmd in SCmd.get_plot_infos():
                continue
            else:
                msg = f'Unknown SCmd!: {code.cmd}'
                LOG.error(msg)
            if is_added:
                is_added = False
                if not is_then:
                    tmp.append('\n')
                    desc_head = '　'
                else:
                    is_then = False
                    desc_head = ''
        return RawData(*tmp)

    def _conv_to_text(self, src: RawData) -> RawData:
        LOG.info('COMP: conv_to_text start')
        tmp = []
        checker = Checker()
        for line in assertion.is_instance(src, RawData).data:
            if isinstance(line, FormatTag):
                tmp.append(line)
            elif checker.is_breakline(line):
                tmp.append(line)
            elif "# CONTENTS" in line:
                continue
            elif checker.has_tag_top(line):
                if line.startswith('_'):
                    continue
                else:
                    tmp.append(line)
            else:
                tmp.append(line)
        return RawData(*tmp)

    def _add_rubi_on_novel(self, src: RawData, rubis: dict) -> RawData:
        LOG.info('COMP: add_rubi_on_novel start')

        tmp = []
        discards = []
        checker = Checker()
        conv = Converter()

        for line in assertion.is_instance(src, RawData).data:
            if isinstance(line, FormatTag) \
                    or checker.has_tag_top(assertion.is_str(line)) \
                    or checker.is_breakline(line) \
                    or checker.has_tag_comment(line):
                tmp.append(line)
            else:
                for key, rubi in rubis.items():
                    if key in discards:
                        continue
                    elif checker.has_rubi_key(line, key):
                        if checker.has_rubi_exclusions(line, assertion.is_instance(rubi, Rubi).exclusions):
                            continue
                        line = conv.add_rubi(line, key, rubi.rubi)
                        if not rubi.is_always:
                            discards.append(key)
                tmp.append(line)
        return RawData(*tmp)

    #
    # private methods (plot)
    #

    def _conv_to_plot(self, src: CodeList) -> RawData:
        LOG.info('COMP: conv_to_plot start')

        conv = Converter()
        tmp = []
        is_added = False
        head_info = ''
        ch_num = ep_num = sc_num = 1

        for code in assertion.is_instance(src, CodeList).data:
            assertion.is_instance(code, SCode)
            # actions
            if code.cmd in SCmd.get_normal_actions():
                continue
            elif code.cmd in SCmd.get_dialogue_actions():
                continue
            # then
            elif code.cmd is SCmd.THEN:
                continue
            # container break
            elif code.cmd in SCmd.get_end_of_containers():
                continue
            # tags
            elif code.cmd in SCmd.get_tags():
                ret, (ch_num, ep_num, sc_num) = self._conv_from_tag(code, head_info,
                        (ch_num, ep_num, sc_num), True)
                if ret:
                    if code.cmd is SCmd.TAG_TITLE and not ret.startswith('#'):
                        tmp.append('\n')
                    tmp.append(FormatTag.SYMBOL_HEAD if code.cmd is SCmd.TAG_SYMBOL else FormatTag.TAG_HEAD)
                    tmp.append(ret)
            # info
            elif code.cmd in SCmd.get_informations():
                if code.cmd is SCmd.INFO_DATA:
                    head_info = self._get_headinfo(code) + ' | T:' + self._get_headinfo_total(code)
                elif code.cmd is SCmd.INFO_CONTENT:
                    tmp.append(self._get_storyinfo(code))
                continue
            # scene control
            elif code.cmd in SCmd.get_scene_controls():
                continue
            # plot control
            elif code.cmd in SCmd.get_plot_infos():
                tmp.append(f'* {conv.to_description(code.script)}')
                is_added = True
            # others
            else:
                LOG.error(f'Unknown SCmd!: {code.cmd}')
            if is_added:
                is_added = False
                tmp.append('\n')
        return RawData(*tmp)

    #
    # privte methods (common)
    #

    def _conv_from_end_container(self, src: SCode) -> str:
        if assertion.is_instance(src, SCode).cmd is SCmd.END_CHAPTER:
            return '\n--------\n'
        elif src.cmd is SCmd.END_EPISODE:
            return '\n\n'
        elif src.cmd is SCmd.END_SCENE:
            return '\n'
        else:
            return ''

    def _conv_from_tag(self, src: SCode, head_info: str, nums: tuple,
            is_comment: bool) -> Tuple[str, tuple]:
        assertion.is_str(head_info)
        tmp = ''
        ch_num, ep_num, sc_num = assertion.is_tuple(nums)
        if assertion.is_instance(src, SCode).cmd is SCmd.TAG_BR:
            tmp = '\n\n'
        elif src.cmd is SCmd.TAG_COMMENT:
            if is_comment:
                if src.option == 'outline':
                    tmp = f'<!--\n【{"。".join(src.script)}】\n-->\n\n'
                else:
                    tmp = f'<!--{"。".join(src.script)}-->\n'
        elif src.cmd is SCmd.TAG_HR:
            tmp = '--------'*9
        elif src.cmd is SCmd.TAG_SYMBOL:
            tmp = f'\n{"".join(src.script)}\n\n'
        elif src.cmd is SCmd.TAG_TITLE:
            if src.option == 'contents':
                tmp = f'---\n# CONTENTS\n{src.script[0]}\n---\n'
            else:
                head = '#' * src.option if isinstance(src.option, int) else '##'
                info_str = f' {head_info}' if head_info else ''
                title = ''.join(src.script)
                head_info = ''
                if src.option == 1:
                    tmp = f'{head} {title}{info_str}\n\n'
                elif src.option == 2:
                    tmp = f'{head} Ch-{ch_num}: {title}{info_str}\n\n'
                    ch_num += 1
                elif src.option == 3:
                    tmp = f'{head} Ep-{ep_num}: {title}{info_str}\n\n'
                    ep_num += 1
                elif src.option == 4:
                    tmp = f'_S-{sc_num} {title}_ {info_str}\n'
                    sc_num += 1
                else:
                    tmp = f'\n{head} {title}\n\n'
        else:
            LOG.debug(f'Other tag: {src.cmd}')
        return (tmp, (ch_num, ep_num, sc_num))

    def _get_headinfo(self, code: SCode) -> str:
        info = assertion.is_instance(
                assertion.is_instance(code, SCode).script[0], HeaderInfo)
        return f'[{info.desc_chars}c / {info.papers:.2f}p ({info.lines:.2f}ls)]'

    def _get_headinfo_total(self, code: SCode) -> str:
        info = assertion.is_instance(
                assertion.is_instance(code, SCode).script[0], HeaderInfo)
        return f'[{info.total_chars}c / {info.total_papers:.2f}p ({info.total_lines:.2f}ls)]'

    def _get_storyinfo(self, src: SCode) -> str:
        info = "".join(assertion.is_instance(src, SCode).script)
        return f"<!-- STORY INFO:\n{info}\n-->\n"
