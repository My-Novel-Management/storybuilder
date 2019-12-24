# -*- coding: utf-8 -*-
"""Define skin class.
"""
from . import assertion
from . import __FASHION_LAYER__, __ITEM_LAYER__, __STAGE_LAYER__
from .action import Action, ActType
from .item import Item
from .person import Person
from .stage import Stage
from .who import Who


class BaseSkin(object):
    def __init__(self, subject, model, attrs: dict, layer: str):
        self._subject = subject
        self._model = model
        self._attrs = assertion.is_dict(attrs)
        self._layer = assertion.is_str(layer)

    @property
    def attrs(self): return self._attrs

    @property
    def subject(self): return self._subject

    @property
    def model(self): return self._model

    @property
    def layer(self): return self._layer

    def addBody(self, *args: str):
        return self._appendVals('body', args)

    def getAction(self, val: str) -> Action:
        return Action(self._subject, val, ActType.BE, layer=self._layer)

    def getBody(self, num: int=0) -> Action:
        return self.getAction(self._attrIfExists('body', num))

    ## privates
    def _appendVals(self, key: str, vals: (str, list, tuple)):
        if not key in self._attrs:
            raise AssertionError(f"Skin has no key: {key}!")
        if isinstance(vals, str):
            self._attrs[key].append(vals)
        else:
            for v in vals:
                self._attrs[key].append(v)
        return self

    def _attrIfExists(self, key: str, num: int) -> str:
        if not key in self._attrs:
            raise AssertionError(f"Skin has no key: {key}!")
        if num < len(self._attrs[key]):
            return self._attrs[key][num]
        else:
            return f"(Unimplemented of {key})"


class PersonSkin(BaseSkin):
    """For a skin:
        - hair
        - face
        - eyes
        - nose
        - mouth
        - hight
        - weight
        - arms
        - legs
    """
    def __init__(self, person: Person):
        super().__init__(assertion.is_instance(person, Person), person,
                {
                'body': [],
                'hair': [],
                'face': [],
                },
                __FASHION_LAYER__)

    @property
    def attrs(self): return self._attrs

    def addFace(self, *args: str):
        return self._appendVals('face', args)

    def addHair(self, *args: str):
        return self._appendVals('hair', args)

    def getFace(self, num: int=0) -> Action:
        return self.getAction(self._attrIfExists('face', num))

    def getHair(self, num: int=0) -> Action:
        return self.getAction(self._attrIfExists('hair', num))


class StageSkin(BaseSkin):

    def __init__(self, stage: Stage):
        super().__init__(Who(), assertion.is_instance(stage, Stage),
                {
                    'body': [],
                },
                __STAGE_LAYER__)


class ItemSkin(BaseSkin):

    def __init__(self, item: Item):
        super().__init__(Who(), assertion.is_instance(item, Item),
                {
                    'body': [],
                },
                __ITEM_LAYER__)
