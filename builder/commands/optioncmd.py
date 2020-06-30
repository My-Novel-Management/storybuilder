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

    #
    # methods
    #

    def get_commandline_arguments(self,
            is_testing: bool=False,
            test_data: list=None) -> argparse.Namespace: # pragma: no cover
        ''' Get and setting a commandline option.

        NOTE:
            -p, --plot: output a plot.
            -r, --rubi: output with rubi.
            -c, --comment: output with comments.
            --console: output to a console.
            --debug: set DEBUG on log leve.
            --forcemecab: specific using travic-ci
            --format: format type for output
            --log: set log level.
            --part: select story parts.
            --priority: set a priority filter.
            --text: output as a text.
        Returns:
            :`ArgumentParser`: commandline options.
        '''
        LOG.info('OPT_PARSE: get commandline arguments: start')
        parser = argparse.ArgumentParser()
        test_data = test_data if test_data else []

        LOG.info('OPT_PARSE: set option arguments')
        parser.add_argument('-c', '--comment', help='output with comments', action='store_true')
        parser.add_argument('-p', '--plot', help='output a plot', action='store_true')
        parser.add_argument('-r', '--rubi', help='output with rubi', action='store_true')
        parser.add_argument('--console', help='output to the console (for debug)', action='store_true')
        parser.add_argument('--debug', help='set DEBUG on log level', action='store_true')
        parser.add_argument('--forcemecab', help='force no use mecab dir', action='store_true')
        parser.add_argument('--format', help='format type for output', type=str)
        parser.add_argument('--log', help='set a log level', type=str)
        parser.add_argument('--part', help='select story parts', type=str)
        parser.add_argument('--priority', help='set a priority filter', type=int)
        parser.add_argument('--text', help='output as a text', action='store_true')

        LOG.info('OPT_PARSE: get option arguments from commandline')
        args = parser.parse_args(args=test_data) if is_testing else parser.parse_args()

        return args

