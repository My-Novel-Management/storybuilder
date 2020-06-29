# -*- coding: utf-8 -*-
'''
Checker Object
==============
'''

from __future__ import annotations

__all__ = ('Checker',)


import re
from typing import Any
from builder.commands.scode import SCode, SCmd
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Checker(object):
    ''' Checker Object class.
    '''

    #
    # methods (has)
    #

    def has_rubi_exclusions(self, src: str, ex_words: (tuple, list)) -> bool:
        ''' Check whether the string has a exclusion rubi-words.
        '''
        for word in assertion.is_listlike(ex_words):
            if assertion.is_str(word) in assertion.is_str(src):
                return True
        return False

    def has_rubi_key(self, src: str, key: str) -> bool:
        ''' Check whether the string has a rubi-key.
        '''
        return True if re.search(r'{}'.format(assertion.is_str(key)), assertion.is_str(src)) else False

    def has_rubi_key_converted(self, src: str, key: str) -> bool:
        ''' Check whether the string has a converted rubi-key.
        '''
        return True if re.search(r'｜{}'.format(assertion.is_str(key)), assertion.is_str(src)) \
                or re.search(r'{《}'.format(key), src) else False

    def has_tag_comment(self, src: str) -> bool:
        ''' Check whether the string has a tag comment.
        '''
        return src.startswith('<!--')

    def has_tag_symbol(self, src: str, symbol: str='$') -> bool:
        ''' Check whether the string has a tag symbol.
        '''
        return True if re.search(r'\{}[a-zA-Z]'.format(assertion.is_str(symbol)), assertion.is_str(src)) else False

    def has_tag_top(self, src: str) -> bool:
        ''' Check whether the string has a tag top.
        '''
        return src.startswith(('# ', '## ', '### ', '**', '_S'))

    def has_then(self, src: SCode) -> bool:
        ''' Check whether the scode script has then.
        '''
        if assertion.is_instance(src, SCode).cmd is SCmd.THEN:
            return True
        return len([val for val in src.script if '&' == val]) > 0

    #
    # methods (is)
    #

    def is_breakline(self, src: str) -> bool:
        return '\n' == src or '\n\n' == src

    def is_empty_script(self, src: SCode, is_ex_comment: bool=False) -> bool:
        tmp_a = [val for val in assertion.is_instance(src, SCode).script if '&' == val]
        tmp_b = [val for val in src.script if val.startswith('#')] if not is_ex_comment else []
        if len(src.script) == 0:
            return True
        elif len(src.script) - len(tmp_a) - len(tmp_b) <= 0:
            return True
        else:
            return False

