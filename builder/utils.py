# -*- coding: utf-8 -*-
"""Define utility methods
"""
from . import assertion
from .action import Action
from .description import Description


def strOfDescription(action: Action, splitter: str="") -> str:
    return f"{splitter}".join(assertion.is_instance(action, Action).description.descs)
