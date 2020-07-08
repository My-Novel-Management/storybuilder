# -*- coding: utf-8 -*-
'''
Script Converter Object
===================
'''

from __future__ import annotations

__all__ = ('ScriptConverter',)

import os
import sys
from builder.commands.optioncmd import OptionParser
from builder.core.outputter import Outputter
from builder.datatypes.outputmode import OutputMode
from builder.datatypes.rawdata import RawData
from builder.datatypes.textlist import TextList
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class ScriptConverter(object):
    ''' Convert a scene file from a text.
    '''
    def to_scenefile(self, srcfile: str, is_debug: bool=False):
        tmp = []
        fname = 'scene'
        suffix = ''
        extention = 'py'
        builddir = 'build'
        mode = OutputMode.CONSOLE if is_debug else OutputMode.FILE
        with open(srcfile) as f:
            tmp = [line.strip() for line in f.readlines()]
        head = self._get_file_header()
        body = self._conv_scene(tmp)
        data = TextList(*[f'{line}\n' for line in head + body])
        Outputter().execute(data, mode, fname, suffix, extention, builddir)

    def _get_file_header(self) -> list:
        tmp = []
        tmp.append('# -*- cofing: utf-8 -*-')
        tmp.append("'''\nStage: xxx\n'''")
        tmp.append('import os')
        tmp.append('import sys')
        tmp.append("sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))")
        tmp.append("sys.path.append('storybuilder')")
        tmp.append('from storybuilder.builder.world import World')
        tmp.append('')
        tmp.append('')
        tmp.append('## scenes')
        return tmp

    def _conv_scene(self, src: list) -> list:
        tmp = []
        in_scene = False
        sc_num = 1
        for line in assertion.is_list(src):
            if line.startswith('#'):
                if in_scene:
                    tmp.extend(self._get_scene_footer())
                tmp.extend(self._get_scene_header(line, sc_num))
                sc_num += 1
                in_scene = True
            elif line == '':
                tmp.append(f'{self._get_tabspace(3)}w.br(),')
            elif line.endswith("。"):
                tmp.append(f'{self._get_tabspace(3)}who.do("{line[:-1]}"),')
            elif line.startswith("「"):
                tmp.append(f'{self._get_tabspace(3)}who.talk("{line[1:-1]}"),')
            elif line.startswith("『"):
                tmp.append(f'{self._get_tabspace(3)}who.voice("{line[1:-1]}"),')
            elif line in ('◆', '※', '　　　　◆', '　　　　※'):
                tmp.append(f'{self._get_tabspace(3)}w.symbol("　　　　{line.strip()}"),')
            else:
                tmp.append(f'{self._get_tabspace(3)}who.do("{line}"),')
        if in_scene:
            tmp.extend(self._get_scene_footer())
        return tmp

    def _get_scene_header(self, title: str, num: int) -> list:
        tmp = []
        tmp.append(f'def sc_{num}(w: World):')
        tmp.append(f'{self._get_tabspace(1)}who = w.get("who")')
        tmp.append(f'{self._get_tabspace(1)}return w.scene("{title}",')
        return tmp

    def _get_scene_footer(self) -> list:
        tmp = []
        tmp.append(f'{self._get_tabspace(3)})')
        tmp.append('')
        return tmp

    def _get_tabspace(self, num: int) -> str:
        return '    ' * assertion.is_int(num)


def main():
    opt = OptionParser()
    opt.parser.add_argument('target', help='target file path', type=str)
    opt_args = opt.get_commandline_arguments()
    LOG.reset_logger(opt_args)
    target = opt_args.target
    is_debug = opt_args.debug
    if not (os.path.exists(f'./{target}') or os.path.exists(target)):
        LOG.critical(f'File not found: {target}')
        return 1
    conv = ScriptConverter()
    conv.to_scenefile(target, is_debug)
    print('>> FINISHED!!')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
