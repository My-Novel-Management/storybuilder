# -*- coding: utf-8 -*-
'''
Custom assertion methods
========================

Usage:

    >>> def foo(val: str):
        _val = assertion.is_str(val) # validated string type
'''

__all__ = ('is_between',
        'is_bool', 'is_dict', 'is_instance', 'is_int', 'is_int_or_str',
        'is_list', 'is_listlike', 'is_str', 'is_subclass', 'is_tuple',
        'is_various_types',
        'is_valid_length',
        )

from typing import Any, Type, TypeVar


# alias
T = TypeVar('T')


# constant
_ERR_INVALID_TYPE = "{} must be {} type."


#
# utility methods (is checker)
#

def is_between(val: int, maxnum: int, minnum: int) -> int:
    ''' Validate a value between max-number and min-number.
    '''
    assert isinstance(val, int)
    assert isinstance(maxnum, int)
    assert isinstance(minnum, int)
    assert val <= maxnum and val >= minnum, f"{val} must be between {maxnum} to {minnum}."
    return val


def is_bool(val: bool) -> bool:
    ''' Validate a value whether is a type of bool.
    '''
    assert isinstance(val, bool), _ERR_INVALID_TYPE.format(_typename_of(val), 'bool')
    return val


def is_dict(val: dict) -> dict:
    ''' Validate a value whether is a type of dict.
    '''
    assert isinstance(val, dict), _ERR_INVALID_TYPE.format(_typename_of(val), 'dict')
    return val


def is_instance(val: T, cls: Type[T]) -> T:
    ''' Validate a value whether is a type of `Type`.
    '''
    assert isinstance(val, cls), _ERR_INVALID_TYPE.format(_typename_of(val), type(cls))
    return val


def is_int(val: int) -> int:
    ''' Validate a value whether is a type of int.
    '''
    assert isinstance(val, int), _ERR_INVALID_TYPE.format(_typename_of(val), 'int')
    return val


def is_int_or_float(val: (int, float)) -> (int, float):
    ''' Validate a value whether is a type of int or float.
    '''
    assert isinstance(val, (int, float)), _ERR_INVALID_TYPE(_typename_of(val), 'int or float')
    return val

def is_int_or_str(val: (int, str)) -> (int, str):
    ''' Validate a value whether is a type of int or str.
    '''
    assert isinstance(val, (int, str)), _ERR_INVALID_TYPE.format(_typename_of(val), 'int or str')
    return val


def is_list(val: list) -> list:
    ''' Validate a value whether is a type of list.
    '''
    assert isinstance(val, list), _ERR_INVALID_TYPE.format(_typename_of(val), 'list')
    return val

def is_listlike(val: (list, tuple)) -> (list, tuple):
    ''' Validate a value whether is a type of list or tuple.
    '''
    assert isinstance(val, list) or isinstance(val, tuple), _ERR_INVALID_TYPE.format(_typename_of(val), 'list')
    return val

def is_str(val: str) -> str:
    ''' Validate a value whether is a type of str.
    '''
    assert isinstance(val, str), _ERR_INVALID_TYPE.format(_typename_of(val), 'str')
    return val


def is_subclass(val: T, cls: Type[T]) -> Any:
    ''' Validate a value whether is a subclass of `Type`
    '''
    assert issubclass(type(val), cls), _ERR_INVALID_TYPE.format(_typename_of(val), f"subclass of {type(cls)}")
    return val


def is_tuple(val: tuple) -> tuple:
    ''' Validate a value whether is a type of tuple.
    '''
    assert isinstance(val, tuple), _ERR_INVALID_TYPE.format(_typename_of(val), 'tuple')
    return val

def is_various_types(val: Any, types: tuple) -> Any:
    ''' Validate a value whether is a type of any `Type`s.
    '''
    assert isinstance(val, types), _ERR_INVALID_TYPE.format(_typename_of(val), f'{types}')
    return val

#
# utility methods (validate)
#

def is_valid_length(val: (list, tuple), length: int) -> (list, tuple):
    ''' Validate a value has the length.
    '''
    assert len(val) == length, f"Invalid the length of {val}: {len(val)}"
    return val


#
# private methods
#
def _typename_of(val: Any) -> str:
    return val.__class__.__name__
