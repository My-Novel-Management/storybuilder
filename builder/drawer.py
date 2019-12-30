# -*- coding: utf-8 -*-
"""Define actor class for expression
"""
## public libs
## local libs
from utils import assertion
from utils import util_tools as util
## local files
from builder.baseactor import BaseActor
from builder.basedata import BaseData
from builder.shot import Shot
from builder.who import Who


class Drawer(BaseActor):
    """The actor class for drawing.
    """
    def __init__(self, src: BaseData=None):
        super().__init__(src if src else Who())

    ## methods
    def paint(self, *args) -> Shot:
        return Shot(*args)

    def paintWithTerm(self, *args) -> Shot:
        return Shot(*args, isTerm=True)

    ## alias
    def p(self, *args) -> Shot:
        return self.paint(*args)

    def pT(self, *args) -> Shot:
        return self.paintWithTerm(*args)
