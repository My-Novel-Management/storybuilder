# -*- coding: utf-8 -*-
'''
Builder Exception Object
========================
'''

from __future__ import annotations

__all__ = ('BuilderException',)


from builder.utils import assertion


class BuilderError(Exception):
    """Base class for exceptions of the story builder"""
    pass

