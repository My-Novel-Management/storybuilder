# -*- coding: utf-8 -*-
'''
File and Filename Utility methods
=================================
'''

__all__ = (
        'get_module_filename',
        )


import inspect
from builder.utils import assertion


def get_module_filename(frame_num: int) -> str:
    frame = inspect.stack()[frame_num]
    module = inspect.getmodule(frame[0])
    return module.__file__
