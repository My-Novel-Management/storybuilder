# -*- coding: utf-8 -*-
"""Assertion methods.

Usage:
    from . import assertion as assertion
    assertion.is_str(string_validated)
"""
from typing import Any


_ERR_INVALID_TYPE = "{} must be {}"


## public methods
def hasKey(key: str, data: dict) -> Any:
    assert key in data, f"'{key}' cannot find in the dictionary data {data}"
    return data[key]

def isBetween(val, max: int, min: int) -> bool:
    assert val <= max and val >= min, f"{val} must be between {max} to {min}"
    return val


def isBool(val) -> bool:
    assert isinstance(val, bool), _ERR_INVALID_TYPE.format(_typename_of(val), "bool")
    return val


def isDict(val) -> dict:
    assert isinstance(val, dict), _ERR_INVALID_TYPE.format(_typename_of(val), "dict")
    return val


def isInstance(val, cls) -> Any:
    assert isinstance(val, cls), _ERR_INVALID_TYPE.format(_typename_of(val), type(cls))
    return val


def isInt(val) -> int:
    assert isinstance(val, int), _ERR_INVALID_TYPE.format(_typename_of(val), "int")
    return val


def isIntOrStr(val) -> [int, str]:
    assert isinstance(val, (int, str)), _ERR_INVALID_TYPE.format(_typename_of(val), "int or str")
    return val


def isList(val, strict: bool=False) -> [list, tuple]:
    assert isinstance(val, list) or not strict and isinstance(val, tuple), _ERR_INVALID_TYPE.format(
            _typename_of(val), "list" if strict else "list(tuple)")
    return val


def isStr(val) -> str:
    assert isinstance(val, str), _ERR_INVALID_TYPE.format(_typename_of(val), "str")
    return val


def isSubclass(val, cls) -> Any:
    assert issubclass(type(val), cls), _ERR_INVALID_TYPE.format(_typename_of(val), f"subclass of {type(cls)}")
    return val


def isTuple(val) -> tuple:
    assert isinstance(val, tuple), _ERR_INVALID_TYPE.format(_typename_of(val), "tuple")
    return val


# private methods
def _typename_of(val) -> str:
    return val.__class__.__name__
