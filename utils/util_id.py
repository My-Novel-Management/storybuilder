# -*- coding: utf-8 -*-
"""Define utility for id.
"""


class UtilityID(object):
    """Useful id utility
    """
    __nextId__ = 1

    @classmethod
    def getNextId(cls) -> int:
        tmp = cls.__nextId__
        cls.__nextId__ += 1
        return tmp
