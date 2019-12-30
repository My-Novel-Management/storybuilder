# -*- coding: utf-8 -*-
"""Define data type for packing
"""
## public libs
from collections import namedtuple
## local libs
from utils import assertion
## local files
from builder.chapter import Chapter
from builder.episode import Episode
from builder.scene import Scene
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


## define data type
DataPack = namedtuple('DataPack', 'head body')


## methods
def titlePacked(src: StoryLike) -> DataPack:
    head = ""
    if isinstance(src, Story):
        head = "story"
    elif isinstance(src, Chapter):
        head = "chapter"
    elif isinstance(src, Episode):
        head = "episode"
    elif isinstance(src, Scene):
        head = "scene"
    return DataPack(f"{head} title", src.title)
