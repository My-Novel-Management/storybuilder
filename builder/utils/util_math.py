# -*- coding: utf-8 -*-
'''
Mathematics Utility methods
===========================
'''

__all__ = ('int_ceil',)


from builder.utils import assertion


def int_ceil(a: int, b: int) -> int:
    ''' Ceil integer
    '''
    return -(-assertion.is_int(a) // assertion.is_int(b))

