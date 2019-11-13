# -*- coding: utf-8 -*-
"""Define utility methods
"""
from . import assertion
from .action import Action
from .description import Description


def strOfDescription(action: Action):
    return "".join(action.description.descs)
