# -*- coding: utf-8 -*-
'''
Script Converter Object
===================
'''

from __future__ import annotations

__all__ = ('ScriptConverter',)

import os
import sys
from builder.core.outputter import Outputter
from builder.datatypes.outputmode import OutputMode
from builder.datatypes.rawdata import RawData
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
        data = RawData(*[f'{line}\n' for line in head + body])
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
            else:
                tmp.append(f'{self._get_tabspace(3)}"{line}",')
        if in_scene:
            tmp.extend(self._get_scene_footer())
        return tmp

    def _get_scene_header(self, title: str, num: int) -> list:
        tmp = []
        tmp.append(f'def sc_{num}(w: World):')
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
    import argparse
    if len(sys.argv) <= 1:
        LOG.critical(f'Not set a converting file')
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='target file path', type=str)
    parser.add_argument('--debug', help='set Debug mode', action='store_true')
    args = parser.parse_args()
    target = args.target
    is_debug = True if args.debug else False
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
