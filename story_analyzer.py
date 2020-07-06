# -*- coding: utf-8 -*-
'''
Story Analyzer Object
=====================
'''

from __future__ import annotations

__all__ = ('StoryAnalyzer',)

from analyzer.analyzer import Analyzer
from builder.commands.optioncmd import OptionParser
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


def main():
    opt = OptionParser()
    opt.parser.add_argument('target', help='target file path', type=str)
    opt_args = opt.get_commandline_arguments()
    LOG.reset_logger(opt_args)
    target = opt_args.target
    person_names = []
    is_debug = opt_args.debug
    analyzer = Analyzer()
    analyzer.execute(target, person_names, is_debug)
    print('>> FINISHED!!')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
