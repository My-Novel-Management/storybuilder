# -*- coding: utf-8 -*-
'''
Datetime Utility methods
========================
'''

__all__ = (
        'get_date_lastmodified',
        )


import os
import datetime
from builder.utils import assertion


def get_date_lastmodified(fname: str) -> datetime.date:
    return datetime.date.fromtimestamp(os.stat(fname).st_mtime)
