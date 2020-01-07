# -*- coding: utf-8 -*-
"""Define class that world management.
"""


class UtilityDict(dict):
    """Useful dictionary class.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

