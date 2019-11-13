# -*- coding: utf-8 -*-
"""The parser.
"""
from itertools import chain
from . import assertion
from .action import Action, ActType
from .story import Story
from .chapter import Chapter
from .episode import Episode
from .scene import Scene, ScenarioType
from .action import Action, ActType, TagAction, TagType
from .who import Who
from .description import Description, DescType, NoDesc
from .basesubject import NoSubject
from .strutils import str_replaced_tag_by_dictionary, str_duplicated_chopped, extraspace_chopped, duplicate_bracket_chop_and_replaceed
from .combaction import CombAction
from .utils import strOfDescription

# define type hint
AllActions = [Action, CombAction, TagAction]
BaseActions = [Action, TagAction]


class Parser(object):
    """Parser class.
    """
    def __init__(self, story: Story, words: dict, priority: int):
        self._story = self._storyConverted(story, words, priority)

    @property
    def story(self): return self._story

    # methods
    def description(self, is_comment: bool):
        return _descriptionsFrom(self.story, is_comment)

    def layer(self):
        return _actionLayersFrom(self.story)

    def outline(self):
        return _outlinesFrom(self.story)

    def scenario(self, is_comment: bool):
        return _scenariosFrom(self.story, is_comment)

    # privates
    def _storyConverted(self, story: Story, words: dict, pri_filter: int):
        ''' NOTE: converted story content
                1) prioriy filter
                2) layer replaced
                3) pronoun replaced
                4) description connected
                5) tag replaced
        '''
        return story_tag_replaced(
                _descriptionConnectedFrom(
                    story_pronoun_replaced(
                        story_layer_replaced(
                            story_filtered_by_priority(story, pri_filter)
                    ))), words
                )

# privates
def _actionLayersFrom(story: Story):
    def _in_action(action: AllActions, head: str):
        if isinstance(action, CombAction):
            return [(v.layer, head, v) for v in action.actions]
        else:
            return [(action.layer, head, action)]

    def _in_scene(scene: Scene, head: str):
        return chain.from_iterable(_in_action(v, f"{head}-{scene.title}") for v in scene.actions)

    def _in_episode(episode: Episode, head: str):
        return chain.from_iterable(_in_scene(v, f"{head}-{episode.title}") for v in episode.scenes)

    def _in_chapter(chapter: Chapter):
        return chain.from_iterable(_in_episode(v, f"{chapter.title}") for v in chapter.episodes)

    return [(f"# {story.title}\n")] \
            + list(chain.from_iterable(_in_chapter(v) for v in story.chapters))

def _descriptionConnectedFrom(story: Story):
    def _in_action(action: AllActions):
        if isinstance(action, CombAction):
            return action.inherited(*[_in_action(v) for v in action.actions])
        elif isinstance(action, TagAction):
            return action
        elif isinstance(action.description, NoDesc):
            return action
        else:
            return action.inherited(desc=str_duplicated_chopped("。".join(action.description.descs)))

    def _in_scene(scene: Scene):
        return scene.inherited(*[_in_action(v) for v in scene.actions])

    def _in_episode(episode: Episode):
        return episode.inherited(*[_in_scene(v) for v in episode.scenes])

    def _in_chapter(chapter: Chapter):
        return chapter.inherited(*[_in_episode(v) for v in chapter.episodes])

    return story.inherited(*[_in_chapter(v) for v in story.chapters])

def _descriptionsFrom(story: Story, is_comment: bool):
    def _in_action(action: AllActions, is_comment: bool):
        if isinstance(action, CombAction):
            return [str_duplicated_chopped(
                duplicate_bracket_chop_and_replaceed(
                extraspace_chopped("".join(chain.from_iterable(_in_action(v, is_comment) for v in action.actions)))))]
        elif isinstance(action, TagAction):
            return [_tagActionConverted(action, is_comment)]
        else:
            if isinstance(action.description, NoDesc):
                return []
            if action.description.desc_type is DescType.DIALOGUE:
                return [str_duplicated_chopped(f"「{strOfDescription(action)}」")]
            elif action.description.desc_type is DescType.COMPLEX:
                return [strOfDescription(action)]
            else:
                return [str_duplicated_chopped(f"　{strOfDescription(action)}。")]

    def _in_scene(scene: Scene, is_comment: bool):
        return [f"\n**{scene.title}**\n"] \
                + list(chain.from_iterable(_in_action(v, is_comment) for v in scene.actions))

    def _in_episode(episode: Episode, is_comment: bool):
        return [f"\n### {episode.title}\n"] \
                + list(chain.from_iterable(_in_scene(v, is_comment) for v in episode.scenes))

    def _in_chapter(chapter: Chapter, is_comment: bool):
        return [f"## {chapter.title}\n"] \
                + list(chain.from_iterable(_in_episode(v, is_comment) for v in chapter.episodes))

    return [f"# {story.title}\n"] \
            + list(chain.from_iterable(_in_chapter(v, is_comment) for v in story.chapters))

def _outlinesFrom(story: Story):
    def _in_scene(scene: Scene):
        return [(f"- {scene.title}", f"{scene.outline}")]

    def _in_episode(episode: Episode):
        return [(f"\n### {episode.title}", f"{episode.outline}\n")] \
                + list(chain.from_iterable(_in_scene(v) for v in episode.scenes))

    def _in_chapter(chapter: Chapter):
        return [(f"## {chapter.title}", "\n")] \
                + list(chain.from_iterable(_in_episode(v) for v in chapter.episodes))

    return [(f"# {story.title}", "\n")] \
            + list(chain.from_iterable(_in_chapter(v) for v in story.chapters))

def _scenariosFrom(story: Story, is_comment: bool):
    def _conv(action: Action):
        if action.act_type is ActType.TALK:
            return [(ScenarioType.DIALOGUE,
                f"{action.subject.name}「{str_duplicated_chopped(action.outline)}」")]
        else:
            return [(ScenarioType.DIRECTION,
                str_duplicated_chopped(f"{action.outline}。"))]

    def _in_action(action: AllActions, is_comment: bool):
        if isinstance(action, CombAction):
            return chain.from_iterable(_in_action(v, is_comment) for v in action.actions)
        elif isinstance(action, TagAction):
            return [(ScenarioType.TAG, _tagActionConverted(action, is_comment))]
        else:
            return _conv(action)

    def _in_scene(scene: Scene, is_comment: bool):
        return [(ScenarioType.TITLE, f"\n**{scene.title}**\n")] \
                + [(ScenarioType.PILLAR, f"◯{scene.stage.name}（{scene.time.name}）")] \
                + list(chain.from_iterable(_in_action(v, is_comment) for v in scene.actions))

    def _in_episode(episode: Episode, is_comment: bool):
        return [(ScenarioType.TITLE, f"\n### {episode.title}\n")] \
                + list(chain.from_iterable(_in_scene(v, is_comment) for v in episode.scenes))

    def _in_chapter(chapter: Chapter, is_comment: bool):
        return [(ScenarioType.TITLE, f"## {chapter.title}\n")] \
                + list(chain.from_iterable(_in_episode(v, is_comment) for v in chapter.episodes))

    return [(ScenarioType.TITLE, f"# {story.title}\n")] \
            + list(chain.from_iterable(_in_chapter(v, is_comment) for v in story.chapters))

def _tagActionConverted(action: TagAction, is_comment: bool) -> str:
    if action.tag_type is TagType.COMMENT and is_comment:
        return f"<!--{action.info}-->"
    elif action.tag_type is TagType.BR:
        return "\n\n"
    elif action.tag_type is TagType.HR:
        return "----" * 8
    elif action.tag_type is TagType.SYMBOL:
        return f"\n{action.info}\n"
    elif action.tag_type is TagType.TITLE:
        num = int(action.subinfo)
        return f"{'#' * num} {action.info}"
    else:
        return ""



def story_filtered_by_priority(story: Story, pri_filter: int):
    return story.inherited(*[_story_chapter_filtered(v, pri_filter) for v in story.chapters if v.priority >= pri_filter])

def story_pronoun_replaced(story: Story):
    return story.inherited(*[_story_pronoun_replaced_in_chapter(v) for v in story.chapters])

def story_tag_replaced(story: Story, words: dict):
    return story.inherited(*[_story_tag_replaced_in_chapter(v, words) for v in story.chapters])

def story_layer_replaced(story: Story):
    def _as_episode(episode: Episode):
        return episode.inherited(*[_layer_replaced_in_scene(v) for v in episode.scenes])
    def _as_chapter(chapter: Chapter):
        return chapter.inherited(*[_as_episode(v) for v in chapter.episodes])
    return story.inherited(*[_as_chapter(v) for v in story.chapters])

# privates
def _desc_in_tagaction(action: TagAction, is_comment: bool) -> list:
    if action.tag_type is TagType.COMMENT and is_comment:
        return [f"<!--{action.info}-->"]
    elif action.tag_type is TagType.BR:
        return ["\n\n"]
    elif action.tag_type is TagType.HR:
        return ["----" * 8]
    elif action.tag_type is TagType.SYMBOL:
        return [f"\n{action.info}\n"]
    elif action.tag_type is TagType.TITLE:
        num = int(action.subinfo)
        return ["{} {}".format("#" * num, action.info)]
    else:
        return []

def _layer_replaced_in_scene(scene: Scene):
    tmp = []
    cur = Action.MAIN_LAYER
    def _sel_layer(act: Action, cur: str):
        return act.setLayer(cur) if act.layer == Action.DEF_LAYER else act
    def _as_combaction(act: CombAction, cur):
        c_tmp = []
        for a in act.actions:
            if isinstance(a, TagAction) and a.tag_type is TagType.SET_LAYER:
                cur = a.info
            else:
                c_tmp.append(_sel_layer(a, cur))
        return act.inherited(*c_tmp), cur
    for v in scene.actions:
        if isinstance(v, CombAction):
            c_tmp, cur = _as_combaction(v, cur)
            tmp.append(c_tmp)
        elif isinstance(v, TagAction) and v.tag_type is TagType.SET_LAYER:
            cur = v.info
        else:
            tmp.append(_sel_layer(v, cur))
    return scene.inherited(*tmp)

def _story_chapter_filtered(chapter: Chapter, pri_filter: int):
    return chapter.inherited(*[_story_episode_filtered(v, pri_filter) for v in chapter.episodes if v.priority >= pri_filter])

def _story_episode_filtered(episode: Episode, pri_filter: int):
    return episode.inherited(*[_story_scene_filtered(v, pri_filter) for v in episode.scenes if v.priority >= pri_filter])

def _story_scene_filtered(scene: Scene, pri_filter: int):
    tmp = []
    def _as_combaction(act: CombAction, pri: int):
        return act.inherited(*[v for v in act.actions if v.priority >= pri])
    for v in scene.actions:
        if isinstance(v, CombAction):
            tmp.append(_as_combaction(v, pri_filter))
        elif v.priority >= pri_filter:
            tmp.append(v)
    return scene.inherited(*tmp)

def _story_pronoun_replaced_in_chapter(chapter: Chapter):
    return chapter.inherited(*[_story_pronoun_replaced_in_episode(v) for v in chapter.episodes])

def _story_pronoun_replaced_in_episode(episode: Episode):
    return episode.inherited(*[_story_pronoun_replaced_in_scene(v) for v in episode.scenes])

def _story_pronoun_replaced_in_scene(scene: Scene):
    tmp = []
    cur_sub = NoSubject()
    for a in scene.actions:
        if isinstance(a, CombAction):
            tmp_c = []
            for v in a.actions:
                if isinstance(v, TagAction):
                    tmp_c.append(v)
                elif isinstance(v.subject, Who):
                    tmp_c.append(v.inherited(subject=cur_sub))
                else:
                    cur_sub = v.subject
                    tmp_c.append(v)
            tmp.append(a.inherited(*tmp_c))
        elif isinstance(a, TagAction):
            tmp.append(a)
        elif isinstance(a.subject, Who):
            tmp.append(a.inherited(subject=cur_sub))
        else:
            cur_sub = a.subject
            tmp.append(a)
    return scene.inherited(*tmp)

def _story_tag_replaced_in_chapter(chapter: Chapter, words: dict):
    return chapter.inherited(*[_story_tag_replaced_in_episode(v, words) for v in chapter.episodes])

def _story_tag_replaced_in_episode(episode: Episode, words: dict):
    return episode.inherited(*[_story_tag_replaced_in_scene(v, words) for v in episode.scenes])

def _story_tag_replaced_in_scene(scene: Scene, words: dict):
    def _as_combaction(act: CombAction, words: dict):
        return act.inherited(*[_story_tag_replaced_in_action(v, words) for v in act.actions])
    return scene.inherited(*[_as_combaction(v, words) if isinstance(v, CombAction) else _story_tag_replaced_in_action(v, words) for v in scene.actions])

def _story_tag_replaced_in_action(act: [Action, TagAction], words: dict):
    if isinstance(act, TagAction):
        return act
    is_nodesc = isinstance(act.description, NoDesc)
    outline = act.outline
    desc = NoDesc() if is_nodesc else "".join(act.description.descs)
    if hasattr(act.subject, "calling"):
        outline = str_replaced_tag_by_dictionary(act.outline, act.subject.calling)
        if not is_nodesc:
            desc = str_replaced_tag_by_dictionary(desc, act.subject.calling)
    outline = str_replaced_tag_by_dictionary(outline, words)
    if not is_nodesc:
        desc = str_replaced_tag_by_dictionary(desc, words)
    if _isInvalidatedTagReplaced(outline): raise AssertionError("Cannot convert tags in:", outline)
    if not is_nodesc and _isInvalidatedTagReplaced(desc): raise AssertionError("Cannot convert tags in:", desc)
    return act.inherited(outline=outline, desc=desc)

## checker
def _isInvalidatedTagReplaced(target: str, prefix: str='$'):
    return prefix in target

