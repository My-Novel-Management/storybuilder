# -*- coding: utf-8 -*-
'''
Option Parser Object
====================
'''

from __future__ import annotations

__all__ = ('OptionParser',)

import argparse
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class OptionParser(object):
    ''' Option Parser Object class.
    '''
    def __init__(self):
        LOG.info('OPT_PARSER: initialize')
        self._parser = argparse.ArgumentParser()

    #
    # property
    #

    @property
    def parser(self) -> argparse.ArgumentParser:
        return self._parser

    #
    # methods
    #

    def get_commandline_arguments(self,
            is_testing: bool=False,
            test_data: list=None) -> argparse.Namespace: # pragma: no cover
        ''' Get and setting a commandline option.

        NOTE:
            -c, --comment: output with comments.
            -d, --data: output a story data.
            -p, --plot: output a plot.
            -r, --rubi: output with rubi.
            -t, --text: output as a text.
            -z, --analyze: output an analyzed result.
            --console: output to a console.
            --debug: set DEBUG on log leve.
            --format: format type for output
            --log: set log level.
            --part: select story parts.
            --priority: set a priority filter.
        Returns:
            :`ArgumentParser`: commandline options.
        '''
        LOG.info('OPT_PARSE: get commandline arguments: start')
        parser = self._parser
        test_data = test_data if test_data else []

        LOG.info('OPT_PARSE: set option arguments')
        parser.add_argument('-c', '--comment', help='output with comments', action='store_true')
        parser.add_argument('-d', '--data', help='output a story data', action='store_true')
        parser.add_argument('-p', '--plot', help='output a plot', action='store_true')
        parser.add_argument('-r', '--rubi', help='output with rubi', action='store_true')
        parser.add_argument('-t', '--text', help='output as a text', action='store_true')
        parser.add_argument('-z', '--analyze', help='output an analyzed result', action='store_true')
        parser.add_argument('--console', help='output to the console (for debug)', action='store_true')
        parser.add_argument('--debug', help='set DEBUG on log level', action='store_true')
        parser.add_argument('--format', help='format type for output', type=str)
        parser.add_argument('--log', help='set a log level', type=str)
        parser.add_argument('--part', help='select story parts', type=str)
        parser.add_argument('--priority', help='set a priority filter', type=int)

        LOG.info('OPT_PARSE: get option arguments from commandline')
        args = parser.parse_args(args=test_data) if is_testing else parser.parse_args()

        return args

