# -*- coding: utf-8 -*-
'''
Utility methods for dictionary
==============================
'''

__all__ = (
        'calling_dict_from',
        'combine_dict',
        'dict_sorted')

from itertools import chain
from typing import Tuple
from builder.utils import assertion


def calling_dict_from(calling: (str, dict), name: str) -> dict:
    ''' Construct a calling dictionary for Person class.
    '''
    from builder.utils.util_str import dict_from_string
    tmp = {}
    if isinstance(calling, dict):
        tmp = calling
    else:
        tmp = dict_from_string(assertion.is_str(calling), ':')
    me = tmp['me'] if 'me' in tmp else '私'
    return combine_dict(tmp, {'S': name, 'M': me})


def combine_dict(a: dict, b: dict) -> dict:
    ''' Combine one dictionary from two dictionaries.
    '''
    return {**assertion.is_dict(a), **assertion.is_dict(b)}


def dict_sorted(origin: dict, is_reverse: bool=False) -> dict:
    ''' Sort dictionary.
    '''
    return dict(
            sorted(assertion.is_dict(origin).items(),
            key=lambda x:x[0], reverse=assertion.is_bool(is_reverse)))
