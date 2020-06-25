# -*- coding: utf-8 -*-
'''
Collecter Object
================
'''

from __future__ import annotations

__all__ = ('Collecter',)


from itertools import chain
from typing import Any
from builder.commands.scode import SCode, SCmd
from builder.containers.chapter import Chapter
from builder.containers.episode import Episode
from builder.containers.scene import Scene
from builder.containers.story import Story
from builder.utils import assertion
from builder.utils.logger import MyLogger


# logger
LOG = MyLogger.get_logger(__name__)
LOG.set_file_handler()


class Collecter(object):
    ''' Collecter Object class.
    '''

    #
    # methods (containers)
    #

    def container_titles(self, src: (Story, Chapter, Episode, Scene)) -> list:
        tmp = []
        tmp.append(f"{self.get_container_level(src)}:{src.title}")
        for child in assertion.is_instance(src, (Story, Chapter, Episode, Scene)).children:
            if isinstance(child, (Chapter, Episode, Scene)):
                tmp.extend(self.container_titles(child))
        return tmp

    def get_container_level(self, src: (Story, Chapter, Episode, Scene)) -> int:
        if isinstance(src, Story):
            return 0
        elif isinstance(src, Chapter):
            return 1
        elif isinstance(src, Episode):
            return 2
        elif isinstance(src, Scene):
            return 3
        else:
            LOG.error(f'Invalid source (story container): {src}')
            return 3
