# -*- coding: utf-8 -*-
"""Define utility for id.
"""
## public libs
## local libs
from utils import assertion


## methods
def intCeiled(a: (int, float), b: (int, float)) -> int:
    return -(-assertion.isInt(a) // assertion.isInt(b))
