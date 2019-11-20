# -*- coding: utf-8 -*-
"""The extractor
"""
from itertools import chain
from . import assertion
from .action import Action, ActType, TagAction, TagType
from .basesubject import NoSubject
from .basedata import NoData
from .chapter import Chapter
from .combaction import CombAction
from .episode import Episode
from .person import Person
from .scene import Scene
from .story import Story


## define type hints
AllActions = (Action, CombAction, TagAction)
BaseActions = (Action, TagAction)
Someone = (Person, NoSubject)
StoryContainers = (Story, Chapter, Episode, Scene)

class Extractor(object):
    """Extractor class.
    """
    def __init__(self, src: StoryContainers):
        self._src = assertion.is_instance(src, StoryContainers)

    @property
    def src(self) -> StoryContainers:
        return self._src

    @property
    def story(self) -> (Story, None):
        return self._src if isinstance(self._src, Story) else None

    @property
    def chapters(self) -> list:
        if self.story:
            return [v for v in self.story.chapters if isinstance(v, Chapter)]
        elif isinstance(self.src, Chapter):
            return [self.src]
        else:
            return []

    @property
    def episodes(self) -> list:
        def _episodes(chapter: Chapter):
            return [v for v in chapter.episodes if isinstance(v, Episode)]
        if self.chapters:
            return list(chain.from_iterable(_episodes(v) for v in self.chapters))
        elif isinstance(self.src, Episode):
            return [self.src]
        else:
            return []

    @property
    def scenes(self) -> list:
        def _scenes(episode: Episode):
            return [v for v in episode.scenes if isinstance(v, Scene)]
        if self.episodes:
            return list(chain.from_iterable(_scenes(v) for v in self.episodes))
        elif isinstance(self.src, Scene):
            return [self.src]
        else:
            return []

    @property
    def actions(self) -> list:
        def _extract_acts(action: AllActions):
            if isinstance(action, CombAction):
                return [v for v in action.actions if isinstance(v, Action)]
            else:
                return [action]
        def _actions(scene: Scene):
            return chain.from_iterable(_extract_acts(v) for v in scene.actions if isinstance(v, AllActions))
        return list(chain.from_iterable(_actions(v) for v in self.scenes))

    @property
    def persons(self) -> list:
        return list(set(v.subject for v in self.actions if hasattr(v, "subject")))

    @property
    def stages(self) -> list:
        return list(set(v.stage for v in self.scenes if not isinstance(v.stage, NoData)))

    @property
    def days(self) -> list:
        return list(set(v.day for v in self.scenes if not isinstance(v.day, NoData)))

    @property
    def times(self) -> list:
        return list(set(v.time for v in self.scenes if not isinstance(v.time, NoData)))
