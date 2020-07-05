# -*- coding: utf-8 -*-
'''
Analyzer Exception Object
=========================
'''

from __future__ import annotations

__all__ = ('AnalyzerException',)


from builder.datatypes.builderexception import BuilderError
from builder.utils import assertion


class AnalyzerError(BuilderError):
    """Base class for exceptions of the story analyzer"""
    pass

