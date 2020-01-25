# -*- coding: utf-8 -*-
"""The utility for builder
"""
## public libs
## local libs
from utils import assertion
## local files
from builder.action import Action
from builder.conjuction import Then


## define methods
def hasThen(action: Action) -> bool:
    return len([v for v in action.data if isinstance(v, Then)]) > 0

