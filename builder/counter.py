# -*- coding: utf-8 -*-
"""Define tool for counting
"""
## public libs
from itertools import chain
## local libs
from utils import assertion
from utils.util_str import kanjiOf
from utils.util_tools import toSomething, intCeiled
## local files
from builder import ActType
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


class Counter(object):
    """The tool for counting something.
    """
    def __init__(self, src: StoryLike):
        self._src = assertion.isInstance(src, StoryLike)

    ## property
    @property
    def src(self) -> StoryLike:
        return self._src

    ## methods
    def countChapter(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=lambda v: len(v.chapters),
                chapterFnc=lambda v: 1,
                episodeFnc=lambda v: 0,
                sceneFnc=lambda v: 0,
                src=src if src else self.src)

    def countEpisode(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=_countEpisodeIn,
                chapterFnc=_countEpisodeInChapter,
                episodeFnc=lambda v: 1,
                sceneFnc=lambda v: 0,
                src=src if src else self.src)

    def countScene(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=_countSceneIn,
                chapterFnc=_countSceneInChapter,
                episodeFnc=_countSceneInEpisode,
                sceneFnc=lambda v: 1,
                src=src if src else self.src)

    def countAction(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=_countActionIn,
                chapterFnc=_countActionInChapter,
                episodeFnc=_countActionInEpisode,
                sceneFnc=_countActionInScene,
                src=src if src else self.src)

    def countActType(self, act_type: ActType, src: StoryLike=None) -> int:
        return toSomething(self,
                act_type,
                storyFnc=_countActTypeIn,
                chapterFnc=_countActTypeInChapter,
                episodeFnc=_countActTypeInEpisode,
                sceneFnc=_countActTypeInScene,
                src=src if src else self.src)

    ## characters
    def countCharsOfDirection(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=_countCharsOfDirectionIn,
                chapterFnc=_countCharsOfDirectionInChapter,
                episodeFnc=_countCharsOfDirectionInEpisode,
                sceneFnc=_countCharsOfDirectionInScene,
                src=src if src else self.src)

    def countCharsOfShot(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=_countCharsOfShotIn,
                chapterFnc=_countCharsOfShotInChapter,
                episodeFnc=_countCharsOfShotInEpisode,
                sceneFnc=_countCharsOfShotInScene,
                src=src if src else self.src)

    def countKanjiOfShot(self, src: StoryLike=None) -> int:
        return toSomething(self,
                storyFnc=_countKanjiOfShotIn,
                chapterFnc=_countKanjiOfShotInChapter,
                episodeFnc=_countKanjiOfShotInEpisode,
                sceneFnc=_countKanjiOfShotInScene,
                src=src if src else self.src)

    ## manupapers
    def countAsManupaperRows(self, column: int, src: StoryLike=None) -> int:
        return toSomething(self,
                column,
                storyFnc=_countAsManupaperRowsIn,
                chapterFnc=_countAsManupaperRowsInChapter,
                episodeFnc=_countAsManupaperRowsInEpisode,
                sceneFnc=_countAsManupaperRowsInScene,
                src=src if src else self.src)


## privates
''' count episode
'''
def _countEpisodeIn(story: Story) -> int:
    return sum(_countEpisodeInChapter(v) for v in story.chapters)

def _countEpisodeInChapter(chapter: Chapter) -> int:
    return len(chapter.episodes)

''' count scene
'''
def _countSceneIn(story: Story) -> int:
    return sum(_countSceneInChapter(v) for v in story.chapters)

def _countSceneInChapter(chapter: Chapter) -> int:
    return sum(_countSceneInEpisode(v) for v in chapter.episodes)

def _countSceneInEpisode(episode: Episode) -> int:
    return len(episode.scenes)

''' count action
'''
def _countActionIn(story: Story) -> int:
    return sum(_countActionInChapter(v) for v in story.chapters)

def _countActionInChapter(chapter: Chapter) -> int:
    return sum(_countActionInEpisode(v) for v in chapter.episodes)

def _countActionInEpisode(episode: Episode) -> int:
    return sum(_countActionInScene(v) for v in episode.scenes)

def _countActionInScene(scene: Scene) -> int:
    return len(scene.actions)

''' count chars in direction
'''
def _countCharsOfDirectionIn(story: Story) -> int:
    return sum(_countCharsOfDirectionInChapter(v) for v in story.chapters)

def _countCharsOfDirectionInChapter(chapter: Chapter) -> int:
    return sum(_countCharsOfDirectionInEpisode(v) for v in chapter.episodes)

def _countCharsOfDirectionInEpisode(episode: Episode) -> int:
    return sum(_countCharsOfDirectionInScene(v) for v in episode.scenes)

def _countCharsOfDirectionInScene(scene: Scene) -> int:
    return sum(_countCharsOfDirectionInAction(v) for v in scene.actions)

def _countCharsOfDirectionInAction(action: Action) -> int:
    return sum(len(v) for v in action.acts if isinstance(v, str))


''' count chars in shot
'''
def _countCharsOfShotIn(story: Story) -> int:
    return sum(_countCharsOfShotInChapter(v) for v in story.chapters)

def _countCharsOfShotInChapter(chapter: Chapter) -> int:
    return sum(_countCharsOfShotInEpisode(v) for v in chapter.episodes)

def _countCharsOfShotInEpisode(episode: Episode) -> int:
    return sum(_countCharsOfShotInScene(v) for v in episode.scenes)

def _countCharsOfShotInScene(scene: Scene) -> int:
    return sum(_countCharsOfShotInAction(v) for v in scene.actions)

def _countCharsOfShotInAction(action: Action) -> int:
    return sum(sum(len(x) for x in v.infos) for v in action.acts if isinstance(v, Shot))

''' count chars as manupaper
'''
def _countAsManupaperRowsIn(story: Story, column: int) -> int:
    return sum(_countAsManupaperRowsInChapter(v, column) for v in story.chapters)

def _countAsManupaperRowsInChapter(chapter: Chapter, column: int) -> int:
    return sum(_countAsManupaperRowsInEpisode(v, column) for v in chapter.episodes)

def _countAsManupaperRowsInEpisode(episode: Episode, column: int) -> int:
    return sum(_countAsManupaperRowsInScene(v, column) for v in episode.scenes)

def _countAsManupaperRowsInScene(scene: Scene, column: int) -> int:
    res = []
    shots = []
    for v in scene.actions:
        tmp = [x for x in v.acts if isinstance(x, Shot)]
        shots.append(tmp)
    shots_expand = list(chain.from_iterable(shots))
    tmp = 0
    for s in shots_expand:
        tmp += sum(len(v) for v in s.infos)
        if s.isTerm:
            res.append(intCeiled(tmp, column))
            tmp = 0
    else:
        res.append(intCeiled(tmp, column))
    return sum(res)

''' count act type
'''
def _countActTypeIn(story: Story, act_type: ActType) -> int:
    return sum(_countActTypeInChapter(v, act_type) for v in story.chapters)

def _countActTypeInChapter(chapter: Chapter, act_type: ActType) -> int:
    return sum(_countActTypeInEpisode(v, act_type) for v in chapter.episodes)

def _countActTypeInEpisode(episode: Episode, act_type: ActType) -> int:
    return sum(_countActTypeInScene(v, act_type) for v in episode.scenes)

def _countActTypeInScene(scene: Scene, act_type: ActType) -> int:
    return len([v for v in scene.actions if v.act_type is act_type])

''' count kanji
'''
def _countKanjiOfShotIn(story: Story) -> int:
    return sum(_countKanjiOfShotInChapter(v) for v in story.chapters)

def _countKanjiOfShotInChapter(chapter: Chapter) -> int:
    return sum(_countKanjiOfShotInEpisode(v) for v in chapter.episodes)

def _countKanjiOfShotInEpisode(episode: Episode) -> int:
    return sum(_countKanjiOfShotInScene(v) for v in episode.scenes)

def _countKanjiOfShotInScene(scene: Scene) -> int:
    shots = []
    for act in scene.actions:
        tmp = [x.infos for x in act.acts if isinstance(x, Shot)]
        shots.append(chain.from_iterable(tmp))
    infos_expand = tuple(chain.from_iterable(shots))
    return sum(len(kanjiOf(v)) for v in infos_expand)

