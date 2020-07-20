# -*- coding: utf-8 -*-
'''
Utility methods for list
========================
'''

__all__ = (
        'except_none_list',
        )

from itertools import chain
from typing import Any
from builder.utils import assertion


def list_without_none(src: (list, tuple)) -> list:
    ''' List without None.
    '''
    return [val for val in assertion.is_listlike(src) if val]

