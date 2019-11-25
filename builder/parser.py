# -*- coding: utf-8 -*-
"""The parser.
"""
from itertools import chain
from . import assertion
from .action import Action, ActType
from .converter import toConvertTagAction
from .story import Story
from .chapter import Chapter
from .converter import toConvertTagAction
from .episode import Episode
from .scene import Scene, ScenarioType
from .action import Action, ActType, TagAction, TagType
from .who import Who
from .person import Person
from .description import Description, DescType, NoDesc
from .basesubject import NoSubject
from .strutils import str_replaced_tag_by_dictionary, str_duplicated_chopped, extraspace_chopped, duplicate_bracket_chop_and_replaceed
from .combaction import CombAction
from .utils import strOfDescription

# define type hint
AllActions = (Action, CombAction, TagAction)
BaseActions = (Action, TagAction)
SomeOnes = (Person, NoSubject)
StoryContainers = (Story, Chapter, Episode, Scene)


class Parser(object): # pragma: no cover
    """Parser class.
    """
    def __init__(self, src: StoryContainers):
        self._src = src

    @property
    def src(self): return self._src

    # methods
    def toDescriptions(self, is_comment: bool) -> list: # pragma: no cover
        return self._toSomething(
                is_comment,
                storyFnc=_toDescriptionsFrom,
                chapterFnc=_toDescriptionsFromChapter,
                episodeFnc=_toDescriptionsFromEpisode,
                sceneFnc=_toDescriptionsFromScene,
                src=self.src
                )

    def toDescriptionsAsLayer(self) -> list: # pragma: no cover
        return self._toSomething(
                "",
                storyFnc=_toDescriptionsAsLayerFrom,
                chapterFnc=_toDescriptionsAsLayerFromChapter,
                episodeFnc=_toDescriptionsAsLayerFromEpisode,
                sceneFnc=_toDescriptionsAsLayerFromScene,
                src=self.src
                )

    def toOutlines(self) -> list: # pragma: no cover
        return self._toSomething(
                storyFnc=_toOutlinesFrom,
                chapterFnc=_toOutlinesFromChapter,
                episodeFnc=_toOutlinesFromEpisode,
                sceneFnc=_toOutlinesFromScene,
                src=self.src
                )

    def toOutlinesAsLayer(self) -> list: # pragme: no cover
        return self._toSomething(
                "",
                storyFnc=_toOutlinesAsLayerFrom,
                chapterFnc=_toOutlinesAsLayerFromChapter,
                episodeFnc=_toOutlinesAsLayerFromEpisode,
                sceneFnc=_toOutlinesAsLayerFromScene,
                src=self.src
                )

    def toScenarios(self) -> list: # pragma: no cover
        return self._toSomething(
                "",
                storyFnc=_toScenariosFrom,
                chapterFnc=_toScenariosFromChapter,
                episodeFnc=_toScenariosFromEpisode,
                sceneFnc=_toScenariosFromScene,
                src=self.src
                )

    def toScenariosAsLayer(self) -> list: # pragma: no cover
        return self._toSomething(
                "",
                storyFnc=_toScenariosAsLayerFrom,
                chapterFnc=_toScenariosAsLayerFromChapter,
                episodeFnc=_toScenariosAsLayerFromEpisode,
                sceneFnc=_toScenariosAsLayerFromScene,
                src=self.src
                )

    ## privates
    def _toSomething(self, *args,
            storyFnc,
            chapterFnc,
            episodeFnc,
            sceneFnc,
            src=None) -> StoryContainers:
        src = src if src else self.src
        if isinstance(src, Story):
            return storyFnc(src, *args)
        elif isinstance(src, Chapter):
            return chapterFnc(src, *args)
        elif isinstance(src, Episode):
            return episodeFnc(src, *args)
        elif isinstance(src, Scene):
            return sceneFnc(src, *args)
        else:
            raise AssertionError("Non-reachable value: ", src)


# privates
def _toDescriptionsFrom(story: Story, is_comment: bool) -> list:
    return [_storyTitleOf(story)] \
            + list(chain.from_iterable(_toDescriptionsFromChapter(v, is_comment) for v in story.chapters))

def _toDescriptionsFromChapter(chapter: Chapter, is_comment: bool) -> list:
    return [_chapterTitleOf(chapter)] \
            + list(chain.from_iterable(_toDescriptionsFromEpisode(v, is_comment) for v in chapter.episodes))

def _toDescriptionsFromEpisode(episode: Episode, is_comment: bool) -> list:
    return [_episodeTitleOf(episode)] \
            + list(chain.from_iterable(_toDescriptionsFromScene(v, is_comment) for v in episode.scenes))

def _toDescriptionsFromScene(scene: Scene, is_comment: bool) -> list:
    return [_sceneTitleOf(scene)] \
            + [x for x in list(chain.from_iterable(_toDescriptionsFromAction(v, is_comment) for v in scene.actions)) if x]

def _toDescriptionsFromAction(action: AllActions, is_comment: bool) -> list:
    if isinstance(action, CombAction):
        return [str_duplicated_chopped(
            duplicate_bracket_chop_and_replaceed(
                extraspace_chopped("".join(
                    chain.from_iterable(
                        _toDescriptionsFromAction(v, is_comment) for v in action.actions)))))]
    elif isinstance(action, TagAction):
        return [toConvertTagAction(action, is_comment)]
    else:
        if isinstance(action.description, NoDesc):
            return []
        if action.description.desc_type is DescType.DIALOGUE:
            return [str_duplicated_chopped(f"「{strOfDescription(action)}」")]
        elif action.description.desc_type is DescType.COMPLEX:
            return [strOfDescription(action)]
        else:
            return [str_duplicated_chopped(f"　{strOfDescription(action)}。")]

def _toDescriptionsAsLayerFrom(story: Story, head: str) -> list:
    return [("__TITLE__", _storyTitleOf(story)),] \
            + list(chain.from_iterable(_toDescriptionsAsLayerFromChapter(v, head) for v in story.chapters))

def _toDescriptionsAsLayerFromChapter(chapter: Chapter, head: str) -> list:
    return list(chain.from_iterable(_toDescriptionsAsLayerFromEpisode(v, f"{chapter.title}") for v in chapter.episodes))

def _toDescriptionsAsLayerFromEpisode(episode: Episode, head: str) -> list:
    return list(chain.from_iterable(_toDescriptionsAsLayerFromScene(v, f"{head}-{episode.title}") for v in episode.scenes))

def _toDescriptionsAsLayerFromScene(scene: Scene, head: str) -> list:
    return list(chain.from_iterable(_toDescriptionsAsLayerFromAction(v, f"{head}-{scene.title}") for v in scene.actions))

def _toDescriptionsAsLayerFromAction(action: AllActions, head: str) -> list:
    layer = action.actions[0].layer if isinstance(action, CombAction) else action.layer
    tmp = _toDescriptionsFromAction(action, False)
    return [(f"{head}:{layer}", tmp[0] if tmp else "")]

def _toOutlinesAsLayerFrom(story: Story, head: str) -> list:
    return [("__TITLE__", _storyTitleOf(story)),] \
            + list(chain.from_iterable(_toOutlinesAsLayerFromChapter(v, head) for v in story.chapters))

def _toOutlinesAsLayerFromChapter(chapter: Chapter, head: str) -> list:
    return list(chain.from_iterable(_toOutlinesAsLayerFromEpisode(v, chapter.title) for v in chapter.episodes))

def _toOutlinesAsLayerFromEpisode(episode: Episode, head: str) -> list:
    return list(chain.from_iterable(_toOutlinesAsLayerFromScene(v, f"{head}-{episode.title}") for v in episode.scenes))

def _toOutlinesAsLayerFromScene(scene: Scene, head: str) -> list:
    return list(chain.from_iterable(_toOutlinesAsLayerFromAction(v, f"{head}-{scene.title}") for v in scene.actions))

def _toOutlinesAsLayerFromAction(action: AllActions, head: str) -> list:
    if isinstance(action, CombAction):
        return list(chain.from_iterable(_toOutlinesAsLayerFromAction(v, head) for v in action.actions))
    elif isinstance(action, TagAction):
        return []
    else:
        return [(f"{head}:{action.layer}", action.outline),]

def _toOutlinesFrom(story: Story) -> list:
    return [_storyTitleOf(story)] \
            + list(chain.from_iterable(_toOutlinesFromChapter(v) for v in story.chapters))

def _toOutlinesFromChapter(chapter: Chapter) -> list:
    return [_chapterTitleOf(chapter)] \
            + list(chain.from_iterable(_toOutlinesFromEpisode(v) for v in chapter.episodes))

def _toOutlinesFromEpisode(episode: Episode) -> list:
    return [_episodeTitleOf(episode), episode.outline] \
            + list(chain.from_iterable(_toOutlinesFromScene(v) for v in episode.scenes))

def _toOutlinesFromScene(scene: Scene) -> list:
    return [_sceneTitleOf(scene), scene.outline] \
            + list(chain.from_iterable(_toOutlinesFromAction(v) for v in scene.actions))

def _toOutlinesFromAction(action: AllActions) -> list:
    # TODO: Action内容をどうするか考える
    return []

def _toScenariosFrom(story: Story, is_comment) -> list:
    return [(ScenarioType.TITLE, _storyTitleOf(story))] \
            + list(chain.from_iterable(_toScenariosFromChapter(v, is_comment) for v in story.chapters))

def _toScenariosFromChapter(chapter: Chapter, is_comment: bool) -> list:
    return [(ScenarioType.TITLE, _chapterTitleOf(chapter))] \
            + list(chain.from_iterable(_toScenariosFromEpisode(v, is_comment) for v in chapter.episodes))

def _toScenariosFromEpisode(episode: Episode, is_comment: bool) -> list:
    return [(ScenarioType.TITLE, _episodeTitleOf(episode))] \
            + list(chain.from_iterable(_toScenariosFromScene(v, is_comment) for v in episode.scenes))

def _toScenariosFromScene(scene: Scene, is_comment: bool) -> list:
    return [(ScenarioType.TITLE, _sceneTitleOf(scene))] \
            + [(ScenarioType.PILLAR, f"{scene.stage.name}:{scene.day.name}:{scene.time.name}")] \
            + list(chain.from_iterable(_toScenariosFromAction(v, is_comment) for v in scene.actions))

def _toScenariosFromAction(action: AllActions, is_comment: bool) -> list:
    if isinstance(action, CombAction):
        return chain.from_iterable(_toScenariosFromAction(v, is_comment) for v in action.actions)
    elif isinstance(action, TagAction):
        return [(ScenarioType.TAG, toConvertTagAction(action, is_comment)),]
    else:
        if action.act_type is ActType.TALK or action.description.desc_type is DescType.DIALOGUE:
            return [(ScenarioType.DIALOGUE, f"{action.subject.name}:{action.outline}"),]
        else:
            return [(ScenarioType.DIRECTION, action.outline)]

def _toScenariosAsLayerFrom(story: Story, head: str) -> list:
    return [("__TITLE__", "", ScenarioType.TITLE, _storyTitleOf(story))] \
            + list(chain.from_iterable(_toScenariosAsLayerFromChapter(v, head) for v in story.chapters))

def _toScenariosAsLayerFromChapter(chapter: Chapter, head: str) -> list:
    return list(chain.from_iterable(_toScenariosAsLayerFromEpisode(v, f"{chapter.title}") for v in chapter.episodes))

def _toScenariosAsLayerFromEpisode(episode: Episode, head: str) -> list:
    return list(chain.from_iterable(_toScenariosAsLayerFromScene(v, f"{head}-{episode.title}") for v in episode.scenes))

def _toScenariosAsLayerFromScene(scene: Scene, head: str) -> list:
    return list(chain.from_iterable(_toScenariosAsLayerFromAction(v, f"{head}-{scene.title}|{scene.stage.name}:{scene.day.name}:{scene.time.name}") for v in scene.actions))

def _toScenariosAsLayerFromAction(action: AllActions, head: str) -> list:
    _head, pillar = head.split('|')
    layer = action.actions[0].layer if isinstance(action, CombAction) else action.layer
    tmp = _toScenariosFromAction(action, False)[0]
    return [(f"{_head}:{layer}", pillar, tmp[0], tmp[1])]

## utility
def _storyTitleOf(story: Story) -> str:
    return f"# {story.title}"

def _chapterTitleOf(chapter: Chapter) -> str:
    return f"## {chapter.title}"

def _episodeTitleOf(episode: Episode) -> str:
    return f"### {episode.title}"

def _sceneTitleOf(scene: Scene) -> str:
    return f"**{scene.title}**"

def _listExceptedNone(target: list) -> list:
    return [v for v in target if v]
