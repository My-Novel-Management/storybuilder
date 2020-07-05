# -*- coding: utf-8 -*-
'''
File and Filename Utility methods
=================================
'''

__all__ = (
        'get_module_filename',
        )


import inspect
import os
from builder.utils import assertion



#
# methods (file name)
#

def get_module_filename(frame_num: int) -> str:
    frame = inspect.stack()[frame_num]
    module = inspect.getmodule(frame[0])
    return module.__file__

#
# methods (file)
#

def is_exist_path(fname: str) -> bool:
    return os.path.exists(fname)


def get_content_from_text_file(fname: str) -> list:
    tmp = []
    if is_exist_path(fname):
        with open(fname) as f:
            tmp = [line.strip() for line in f.readlines()]
    return tmp

