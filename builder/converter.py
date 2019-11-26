# -*- coding: utf-8 -*-
"""Define Converter class.
"""
from typing import Optional, Tuple
from . import assertion
from .action import Action, ActType, TagAction, TagType
from .basesubject import NoSubject
from .chapter import Chapter
from .combaction import CombAction
from .description import Description, NoDesc
from .episode import Episode
from .person import Person
from .scene import Scene
from .story import Story
from .strutils import str_duplicated_chopped
from .strutils import str_replaced_tag_by_dictionary
from .who import Who
from .utils import strOfDescription


## defines
AllActions = (Action, TagAction, CombAction)
StoryContainers = (Story, Chapter, Episode, Scene)
SomeOnes = (Person, NoSubject)


class Converter(object):
    """The convert a story to tags, pronoouns and more.
    """
    def __init__(self, src: StoryContainers):
        self._src = assertion.is_instance(src, StoryContainers)

    @property
    def src(self) -> StoryContainers:
        return self._src

    def toConnectDescriptions(self, src=None) -> StoryContainers:
        return self._toSomething(
                storyFnc=_toConnectDescsFrom,
                chapterFnc=_toConnectDescsFromChapter,
                episodeFnc=_toConnectDescsFromEpisode,
                sceneFnc=_toConnectDescsFromScene,
                src=src
                )

    def toConverFullSrc(self, pri_filter: int, words: dict, src=None) -> StoryContainers:
        return self.toReplaceTag(words,
                self.toConnectDescriptions(
                self.toReplacePronoun(
                self.toLayer(
                self.toFilter(pri_filter, src=src if src else self.src)))))

    def toFilter(self, pri_filter: int, src=None) -> StoryContainers:
        return self._toSomething(
                pri_filter,
                storyFnc=_toFilterFrom,
                chapterFnc=_toFilterFromChapter,
                episodeFnc=_toFilterFromEpisode,
                sceneFnc=_toFilterFromScene,
                src=src
                )

    def toLayer(self, src=None) -> StoryContainers:
        return self._toSomething(
                storyFnc=_toLayerFrom,
                chapterFnc=_toLayerFromChapter,
                episodeFnc=_toLayerFromEpisode,
                sceneFnc=_toLayerFromScene,
                src=src
                )

    def toReplacePronoun(self, src=None) -> StoryContainers:
        return self._toSomething(
                storyFnc=_toReplacePronounFrom,
                chapterFnc=_toReplacePronounFromChapter,
                episodeFnc=_toReplacePronounFromEpisode,
                sceneFnc=_toReplacePronounFromScene,
                src=src
                )

    def toReplaceTag(self, words: dict, src=None) -> StoryContainers:
        prefix = "$"
        return self._toSomething(
                words, prefix,
                storyFnc=_toReplaceTagFrom,
                chapterFnc=_toReplaceTagFromChapter,
                episodeFnc=_toReplaceTagFromEpisode,
                sceneFnc=_toReplaceTagFromScene,
                src=src
                )

    ## private methods
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

## publics
def toConvertTagAction(action: TagAction, is_comment: bool) -> str:
    if assertion.is_instance(action, TagAction).tag_type is TagType.COMMENT and is_comment:
        return f"<!--{action.info}-->"
    elif action.tag_type is TagType.BR:
        return f"\n\n"
    elif action.tag_type is TagType.HR:
        return "--------" * 8
    elif action.tag_type is TagType.SYMBOL:
        return f"\n{action.info}\n"
    elif action.tag_type is TagType.TITLE:
        return "\n{} {}\n".format('#' * int(action.subinfo), action.info)
    else:
        return ""

## privates
def _toConnectDescsFrom(story: Story) -> Story:
    return story.inherited(
            *generatedValidList([_toConnectDescsFromChapter(v) for v in story.chapters]))

def _toConnectDescsFromChapter(chapter: Chapter) -> Chapter:
    return chapter.inherited(
            *generatedValidList([_toConnectDescsFromEpisode(v) for v in chapter.episodes]))

def _toConnectDescsFromEpisode(episode: Episode) -> Episode:
    return episode.inherited(
            *generatedValidList([_toConnectDescsFromScene(v) for v in episode.scenes]))

def _toConnectDescsFromScene(scene: Scene) -> Scene:
    return scene.inherited(
            *generatedValidList([_toConnectDescsFromAction(v) for v in scene.actions]))

def _toConnectDescsFromAction(action: AllActions) -> AllActions:
    if isinstance(action, CombAction):
        return action.inherited(*[_toConnectDescsFromAction(v) for v in action.actions])
    elif isinstance(action, TagAction):
        return action
    else:
        return action.inherited(
                desc=str_duplicated_chopped(strOfDescription(action, "。")))

def _toFilterFrom(story: Story, pri_filter: int) -> Optional[Story]:
    return story.inherited(
            *generatedValidList([_toFilterFromChapter(v, pri_filter) for v in story.chapters])
            ) if story.priority >= pri_filter else None

def _toFilterFromChapter(chapter: Chapter, pri_filter: int) -> Optional[Chapter]:
    return chapter.inherited(
            *generatedValidList([_toFilterFromEpisode(v, pri_filter) for v in chapter.episodes])
            ) if chapter.priority >= pri_filter else None

def _toFilterFromEpisode(episode: Episode, pri_filter: int) -> Optional[Episode]:
    return episode.inherited(
            *generatedValidList([_toFilterFromScene(v, pri_filter) for v in episode.scenes])
            ) if episode.priority >= pri_filter else None

def _toFilterFromScene(scene: Scene, pri_filter: int) -> Optional[Scene]:
    return scene.inherited(
            *generatedValidList([_toFilterFromAction(v, pri_filter) for v in scene.actions])
            ) if scene.priority >= pri_filter else None

def _toFilterFromAction(action: AllActions,
        pri_filter: int) -> (Optional[Action], Optional[TagAction], Optional[CombAction]):
    return action if action.priority >= pri_filter else None

def _toLayerFrom(story :Story) -> Story:
    return story.inherited(*[_toLayerFromChapter(v) for v in story.chapters])

def _toLayerFromChapter(chapter: Chapter) -> Chapter:
    return chapter.inherited(*[_toLayerFromEpisode(v) for v in chapter.episodes])

def _toLayerFromEpisode(episode: Episode) -> Episode:
    return episode.inherited(*[_toLayerFromScene(v) for v in episode.scenes])

def _toLayerFromScene(scene: Scene) -> Scene:
    tmp = []
    cur = Action.MAIN_LAYER
    for v in scene.actions:
        act, cur = _toLayerFromAction(v, cur)
        tmp.append(act)
    return scene.inherited(*tmp)

def _toLayerFromAction(action: AllActions,
        layer: str) -> (Tuple[Action, str], Tuple[TagAction, str], Tuple[CombAction, str]):
    def _set_layer(action: AllActions, layer: str):
        return action.setLayer(layer) if action.layer == Action.DEF_LAYER or action.layer != layer else action
    if isinstance(action, CombAction):
        tmp = []
        cur = layer
        for v in action.actions:
            act, cur = _toLayerFromAction(v, cur)
            tmp.append(act)
        return action.inherited(*tmp), cur
    elif isinstance(action, TagAction):
        cur = Action.MAIN_LAYER
        if action.tag_type is TagType.SET_LAYER:
            if action.info == Action.DEF_LAYER:
                cur = Action.MAIN_LAYER
            else:
                cur = action.info
        tmp = action.setLayer(cur)
        return tmp, tmp.layer
    else:
        tmp = _set_layer(action, layer)
        return tmp, tmp.layer

def _toReplacePronounFrom(story: Story) -> Story:
    return story.inherited(
            *generatedValidList(_toReplacePronounFromChapter(v) for v in story.chapters)
            )

def _toReplacePronounFromChapter(chapter: Chapter) -> Chapter:
    return chapter.inherited(
            *generatedValidList([_toReplacePronounFromEpisode(v) for v in chapter.episodes])
            )

def _toReplacePronounFromEpisode(episode: Episode) -> Episode:
    return episode.inherited(
            *generatedValidList([_toReplacePronounFromScene(v) for v in episode.scenes])
            )

def _toReplacePronounFromScene(scene: Scene) -> Scene:
    tmp = []
    cur = NoSubject()
    for v in scene.actions:
        act, cur = _toReplacePronounFromAction(v, cur)
        tmp.append(act)
    return scene.inherited(*tmp)

def _toReplacePronounFromAction(action: AllActions,
        subject: SomeOnes) -> (Tuple[Action, Person], Tuple[Action, NoSubject],
                Tuple[TagAction, Person], Tuple[TagAction, NoSubject],
                Tuple[CombAction, Person], Tuple[CombAction, NoSubject]):
    if isinstance(action, CombAction):
        tmp = []
        cur = subject
        for v in action.actions:
            act, cur = _toReplacePronounFromAction(v, cur)
            tmp.append(act)
        return action.inherited(*tmp), cur
    elif isinstance(action, TagAction):
        return action, subject
    else:
        return (action.inherited(subject=subject),
                subject) if isinstance(action.subject, Who) else (action, action.subject)

def _toReplaceTagFrom(story: Story, words: dict, prefix: str) -> Story:
    return story.inherited(
            *[_toReplaceTagFromChapter(v, words, prefix) for v in story.chapters])

def _toReplaceTagFromChapter(chapter: Chapter, words: dict, prefix: str) -> Chapter:
    return chapter.inherited(
            *[_toReplaceTagFromEpisode(v, words, prefix) for v in chapter.episodes])

def _toReplaceTagFromEpisode(episode: Episode, words: dict, prefix: str) -> Episode:
    return episode.inherited(
            *[_toReplaceTagFromScene(v, words, prefix) for v in episode.scenes])

def _toReplaceTagFromScene(scene: Scene, words: dict, prefix: str) -> Scene:
    return scene.inherited(
            *[_toReplaceTagFromAction(v, words, prefix) for v in scene.actions])

def _toReplaceTagFromAction(action: AllActions, words: dict, prefix: str) -> AllActions:
    def _in_outline(act: Action, words: dict):
        return _toReplaceTagInDocument(act.subject, act.outline, words, "outline", prefix)
    def _in_descs(act: Action, words: dict):
        if isinstance(act.description, NoDesc):
            return act.description
        else:
            return _toReplaceTagInDocument(act.subject, strOfDescription(action), words,
                    "description", prefix)
    if isinstance(action, CombAction):
        return action.inherited(
                *[_toReplaceTagFromAction(v, words, prefix) for v in action.actions]
                )
    elif isinstance(action, TagAction):
        return action
    else:
        return action.inherited(
                outline=_in_outline(action, words),
                desc=_in_descs(action, words),
                )

def _toReplaceTagInDocument(subject: SomeOnes, target: str, words: dict,
        msg: str, prefix: str="$") -> str:
    if not prefix in target:
        return target
    tmp = target
    if hasattr(subject, "calling"):
        tmp = str_replaced_tag_by_dictionary(tmp, subject.calling)
    tmp = str_replaced_tag_by_dictionary(tmp, words)
    if isInvalidTagReplaced(tmp, prefix):
        raise AssertionError(f"Cannot convert tag in {msg}: ", tmp)
    return tmp

## utility
def generatedValidList(vals: list) -> list: # pragma: no cover
    return [v for v in vals if v]

def isInvalidTagReplaced(target: str, prefix: str) -> bool: # pragma: no cover
    return prefix in target