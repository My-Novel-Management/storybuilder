# -*- coding: utf-8 -*-
'''
Converter Object
================
'''

from __future__ import annotations

__all__ = ('Converter',)


import re
from typing import Any
from builder.utils import assertion
from builder.utils.logger import MyLogger
from builder.utils.util_str import validate_string_duplicate_chopped


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Converter(object):
    ''' Converter Object class.
    '''

    #
    # methods (description)
    #

    def add_rubi(self, src: str, key: str, rubi: str, num: int=1) -> str:
        return re.sub(r'{}'.format(key), r'{}'.format(rubi), src, num)

    def to_description(self, src: (list, tuple)) -> str:
        _ = "。".join(assertion.is_listlike(src))
        return validate_string_duplicate_chopped(f'{_}。')

    def to_dialogue(self, src: (list, tuple), brackets: tuple=('「', '」')) -> str:
        _ = "。".join(assertion.is_listlike(src))
        return validate_string_duplicate_chopped(f'{brackets[0]}{_}{brackets[1]}')

    def script_relieved_strings(self, src: (list, tuple)) -> list:
        return list(val for val in assertion.is_listlike(src) if isinstance(val, (int, str)))
    def script_relieved_symbols(self, src: (list, tuple)) -> list:
        return list(val for val in assertion.is_listlike(src) if not ('&' == val or '#' in val))

