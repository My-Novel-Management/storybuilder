# -*- coding: utf-8 -*-
"""Define data type of layer
"""
## public libs
## local libs
from utils import assertion
from utils.util_str import tupleEvenStr
## local files
from builder.basedata import BaseData


class Layer(BaseData):
    """The data class of layer.

    Attributes:
        name (str): a layer name
        words (str, tuple): layer words
    """
    def __init__(self, name: str, words: (str, list, tuple)):
        super().__init__(name, assertion.isTuple(tupleEvenStr(words)))

