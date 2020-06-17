# -*- coding: utf-8 -*-
'''
Tag Command Object
==================
'''

from __future__ import annotations

__all__ = ('TagCmd',)


from builder.commands.command import SCmd
from builder.commands.scode import SCode
from builder.datatypes.builderexception import BuilderError
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class TagCmdError(BuilderError):
    ''' General TagCmd Error.
    '''
    pass


class TagCmd(object):
    ''' Tag Command Object class.
    '''

    def __init__(self):
        LOG.info('TCMD: initialize')

    #
    # methods
    #

    def br(self) -> SCode:
        return SCode(None, SCmd.TAG_BR, ())

    def comment(self, *comments: str):
        return SCode(None, SCmd.TAG_COMMENT, comments)

    def hr(self):
        return SCode(None, SCmd.TAG_HR, ())

    def symbol(self, symbol: str):
        return SCode(None, SCmd.TAG_SYMBOL, (symbol,))

    def title(self, title: str):
        return SCode(None, SCmd.TAG_TITLE, (title,))

