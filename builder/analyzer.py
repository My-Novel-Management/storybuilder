# -*- coding: utf-8 -*-
"""The analyze tool.
"""
import re
from collections import Counter
from itertools import chain
import MeCab
from . import assertion
from . import world as wd
from .scene import Scene
from .episode import Episode
from .chapter import Chapter
from .combaction import CombAction
from .action import Action, ActType, TagAction, TagType
from .description import Description, DescType, NoDesc
from .flag import Flag, NoFlag, NoDeflag
from .person import Person
from .chara import Chara
from .basesubject import NoSubject
from .story import Story
from .utils import strOfDescription


## define type
AllActions = [Action, CombAction, TagAction]
BaseActions = [Action, TagAction]
TargetPerson = [Person, Chara, NoSubject]
AllFlags = [Flag, NoFlag, NoDeflag]


class Analyzer(object):
    """The story analyze tools.
    """
    DEF_BASEMENT = 10
    DEF_BASEROWS = 20
    DEF_BASECOLUMNS = 20

    def __init__(self, dic: str):
        self.tokenizer = MeCab.Tagger(dic)
        # NOTE: mecab hack
        self.tokenizer.parse('')

    # main analyzing methods
    def action_percent(self, story):
        acttypes = self.acttypesFrom(story)
        total = sum(v for v in acttypes.values())
        def percent(char, atype):
            return "- {}: {:.2f}%".format(
                    char,
                    acttypes[atype] / total * 100 if total else 0
                    )
        return ["## Actions",
                f"- Total: {total}",
                percent("Act", ActType.ACT),
                percent("Be", ActType.BE),
                percent("Come", ActType.COME),
                percent("Go", ActType.GO),
                percent("Have", ActType.HAVE),
                percent("Hear", ActType.HEAR),
                percent("Look", ActType.LOOK),
                percent("Move", ActType.MOVE),
                percent("Talk", ActType.TALK),
                percent("Think", ActType.THINK),
                ]

    def characters_count(self, story: wd.Story):
        # TODO: outline文字数／シナリオ用
        rows, columns = Analyzer.DEF_BASEROWS, Analyzer.DEF_BASECOLUMNS
        total = _descriptionCountIn(story) # NOTE: 総文字数
        outline = _outlineCountsIn(story) # NOTE: outline文字数
        estimated = self._descs_estimated_count(story) # NOTE: 予想文字数
        manupapers, manupprows = _descriptionManupaperCountsIn(story, rows, columns) # NOTE: 原稿用紙換算枚数
        outlinepapers, outlinerows = _outlineManupaperCountsIn(story, rows, columns) # NOTE: outline原稿用紙換算枚数
        return [
                "## Characters",
                f"- Total: {total} / Outline: {outline}",
                f"- Estimated: {estimated}",
                f"- Manupapers: {manupapers:0.3f}p ({manupprows:0.2f}) / Outline {outlinepapers:0.3f}p ({outlinerows:0.2f}) / {rows} x {columns}",
                ]

    def characters_count_each_scenes(self, story: wd.Story):
        tmp = []
        rows = Analyzer.DEF_BASEROWS
        columns = Analyzer.DEF_BASECOLUMNS
        ch_num = 1
        epi_num = 1
        scene_num = 1
        def _shorttitle(title: str):
            return title[:8] + '..' if len(title) >= 8 else title
        for c in story.chapters:
            tmp.append(f"### CH-{ch_num}: {c.title}")
            ch_num += 1
            for e in c.episodes:
                tmp.append(f"* Ep-{epi_num}: {e.title}")
                epi_num += 1
                for s in e.scenes:
                    total = _descriptionCountInScene(s)
                    _rows = _descriptionManupaperCountsInScene(s, columns)
                    _papers = _rows / rows
                    outline = _outlineCountsInScene(s)
                    _outrows = _outlineManupaperCountsInScene(s, columns)
                    _outpapers = _outrows / rows
                    tmp.append(f"    - {scene_num}. {_shorttitle(s.title)}: {total} [{_papers:0.3f}p ({_rows:0.2f})] / Outline {outline} [{_outpapers:0.3f}p ({_outrows:0.2f})]")
                    scene_num += 1
        return tmp

    def acttypesFrom(self, story: wd.Story):
        acttypes = [ActType.ACT, ActType.BE, ActType.COME, ActType.GO, ActType.HAVE, ActType.HEAR,
                ActType.LOOK, ActType.MOVE, ActType.TALK, ActType.THINK]
        return dict([(v, _acttypeCountsIn(story, v)) for v in acttypes])

    def flag_infos(self, story: Story):
        allflags = _flagsIn(story)
        flags = list(v for v in allflags if not v.isDeflag)
        deflags = list(v for v in allflags if v.isDeflag)
        return ["## Flag info",
                "- flags: {}".format(len(flags)),
                "- deflags: {}".format(len(deflags))] \
                + ["### Flag detail"] \
                + list("+ " + v.info for v in flags) \
                + ["### Deflag detail"] \
                + list("- " + v.info for v in deflags)

    def frequency_words(self, story: wd.Story):
        from .parser import descriptions_from
        is_comment = False
        descs = descriptions_from(story, is_comment)
        parsed = self.tokenizer.parse("\n".join(descs)).split("\n")
        tokens = (re.split('[\t,]', v) for v in parsed)
        def base_excepted(target: str):
            return target in ('EOS', '', 't', 'ー')
        verbs = []
        nouns = []
        adjectives = []
        adverbs = []
        conjuctions = []
        for v in tokens:
            if base_excepted(v[0]):
                continue
            elif len(v) == 1:
                continue
            elif v[1] == '名詞':
                nouns.append(v[0])
            elif v[1] == '動詞':
                verbs.append(v[0])
            elif v[1] == '形容詞':
                adjectives.append(v[0])
            elif v[1] == '副詞':
                adverbs.append(v[0])
            elif v[1] == '接続詞':
                conjuctions.append(v[0])
        noun_counter = Counter(nouns)
        verb_counter = Counter(verbs)
        adject_counter = Counter(adjectives)
        adverb_counter = Counter(adverbs)
        conjuct_counter = Counter(conjuctions)
        def _as_one_counts(counter: Counter):
            return ["others: " + ",".join([word for word, count in counter.most_common() if count == 1])]
        def _wordslist(counter: Counter):
            return [f"{word}: {count}" for word, count in counter.most_common() if count > 1]
        return ["## Frequency words"] \
                + ["\n### 名詞\n"] + [f"{word}: {count}" for word, count in noun_counter.most_common() if not "#" in word and not "*" in word and count > 1] \
                + _as_one_counts(noun_counter) \
                + ["\n### 動詞\n"] + _wordslist(verb_counter) \
                + _as_one_counts(verb_counter) \
                + ["\n### 形容詞\n"] + _wordslist(adject_counter) \
                + _as_one_counts(adject_counter) \
                + ["\n### 副詞\n"] + _wordslist(adverb_counter) \
                + _as_one_counts(adverb_counter) \
                + ["\n### 接続詞\n"] + _wordslist(conjuct_counter) \
                + _as_one_counts(conjuct_counter)

    def dialogue_infos(self, story: Story):
        def _conv(data: list, target: TargetPerson):
            return [f"{target.name}"] + [f"- {v}" for v in data if v]
        charalist = list(set(_personsIn(story)))
        dial_counts = [f"{v.name}: {_dialogueCountIn(story, v)}" for v in charalist]
        each_charas = list(chain.from_iterable(_conv(_dialoguesOfPersonIn(story, v), v) for v in charalist))
        return ["## Dialogue counts\n"] \
                + dial_counts \
                + ["\n## Dialogue each persons\n"] \
                + each_charas

    # privates (hook)
    def _descs_estimated_count(self, story: wd.Story, basement: int=DEF_BASEMENT):
        tmp = self.acttypesFrom(story)
        return sum([
            tmp[ActType.ACT] * 4,
            tmp[ActType.BE] * 1,
            tmp[ActType.COME] * 2,
            tmp[ActType.GO] * 2,
            tmp[ActType.HAVE] * 2,
            tmp[ActType.HEAR] * 2,
            tmp[ActType.LOOK] * 4,
            tmp[ActType.MOVE] * 2,
            tmp[ActType.TALK] * 4,
            tmp[ActType.THINK] * 4,
                ]) * basement

    def _descs_manupaper_counts(self, story: wd.Story, rows: int, columns: int):
        return _manupapers_count(story, rows, columns)

# privates (detail)
def _personsIn(story: Story) -> list:
    def _in_action(action: AllActions):
        if isinstance(action, CombAction):
            return list(chain.from_iterable(_in_action(v) for v in action.actions))
        elif isinstance(action, TagAction):
            return []
        else:
            return [action.subject]

    def _in_scene(scene: Scene):
        return chain.from_iterable(_in_action(v) for v in scene.actions)

    def _in_episode(episode: Episode):
        return chain.from_iterable(_in_scene(v) for v in episode.scenes)

    def _in_chapter(chapter: Chapter):
        return chain.from_iterable(_in_episode(v) for v in chapter.episodes)

    return list(chain.from_iterable(_in_chapter(v) for v in story.chapters))

def _descriptionCountIn(story: Story) -> int:
    def _in_episode(episode: Episode):
        return sum(_descriptionCountInScene(v) for v in episode.scenes)

    def _in_chapter(chapter: Chapter):
        return sum(_in_episode(v) for v in chapter.episodes)

    return sum(_in_chapter(v) for v in story.chapters)

def _descriptionCountInScene(scene: Scene) -> int:
    def _in_action(action: AllActions):
        if isinstance(action, CombAction):
            return sum(_in_action(v) for v in action.actions)
        elif isinstance(action, TagAction):
            return 0
        else:
            return len("".join(action.description.descs))
    return sum(_in_action(v) for v in scene.actions)

def _dialogueCountIn(story: Story, target: TargetPerson) -> int:
    def _in_action(action: AllActions, target: TargetPerson):
        if isinstance(action, CombAction):
            return sum(_in_action(v, target) for v in action.actions)
        elif isinstance(action, TagAction):
            return 0
        else:
            return action.act_type is ActType.TALK and action.subject is target

    def _in_scene(scene: Scene, target: TargetPerson):
        return sum(_in_action(v, target) for v in scene.actions)

    def _in_episode(episode: Episode, target: TargetPerson):
        return sum(_in_scene(v, target) for v in episode.scenes)

    def _in_chapter(chapter: Chapter, target: TargetPerson):
        return sum(_in_episode(v, target) for v in chapter.episodes)

    return sum(_in_chapter(v, target) for v in story.chapters)

def _dialoguesOfPersonIn(story: Story, target: TargetPerson) -> list:
    def _in_action(action: AllActions, target: TargetPerson):
        if isinstance(action, CombAction):
            return chain.from_iterable(_in_action(v, target) for v in action.actions)
        elif isinstance(action, TagAction):
            return []
        else:
            return [strOfDescription(action)] if action.act_type is ActType.TALK and action.subject is target else []

    def _in_scene(scene: Scene, target: TargetPerson):
        return chain.from_iterable(_in_action(v, target) for v in scene.actions)

    def _in_episode(episode: Episode, target: TargetPerson):
        return chain.from_iterable(_in_scene(v, target) for v in episode.scenes)

    def _in_chapter(chapter: Chapter, target: TargetPerson):
        return chain.from_iterable(_in_episode(v, target) for v in chapter.episodes)

    return list(chain.from_iterable(_in_chapter(v, target) for v in story.chapters))

def _flagsIn(story: Story) -> list:
    def _is_flag_or_deflag(flag: AllFlags):
        return not isinstance(flag, (NoFlag, NoDeflag)) or not isinstance(flag, (NoFlag, NoDeflag))

    def _in_action(action: AllActions):
        if isinstance(action, CombAction):
            return chain.from_iterable(_in_action(v) for v in action.actions)
        elif isinstance(action, TagAction):
            return []
        else:
            return [v for v in (action.getFlag(), action.getDeflag()) if _is_flag_or_deflag(v)]

    def _in_scene(scene: Scene):
        return chain.from_iterable(_in_action(v) for v in scene.actions)

    def _in_episode(episode: Episode):
        return chain.from_iterable(_in_scene(v) for v in episode.scenes)

    def _in_chapter(chapter: Chapter):
        return chain.from_iterable(_in_episode(v) for v in chapter.episodes)

    return list(chain.from_iterable(_in_chapter(v) for v in story.chapters))

def _outlineCountsIn(story: Story):
    def _in_episode(episode: Episode):
        return sum(_outlineCountsInScene(v) for v in episode.scenes)

    def _in_chapter(chapter: Chapter):
        return sum(_in_episode(v) for v in chapter.episodes)

    return sum(_in_chapter(v) for v in story.chapters)

def _outlineCountsInScene(scene: Scene):
    def _in_action(action: AllActions):
        if isinstance(action, CombAction):
            return sum(_in_action(v) for v in action.actions)
        elif isinstance(action, TagAction):
            return 0
        else:
            return len(action.outline)
    return sum(_in_action(v) for v in scene.actions)

def _outlineManupaperCountsIn(story: Story, rows: int, columns: int) -> tuple:
    def _in_episode(episode: Episode, columns: int):
        return sum(_outlineManupaperCountsInScene(v, columns) for v in episode.scenes)

    def _in_chapter(chapter: Chapter, columns: int):
        return sum(_in_episode(v, columns) for v in chapter.episodes)

    row_nums = sum(_in_chapter(v, columns) for v in story.chapters)
    papers = row_nums / rows
    return (papers, row_nums)

def _outlineManupaperCountsInScene(scene: Scene, columns: int) -> int:
    def _in_action(action: AllActions, columns: int):
        if isinstance(action, CombAction):
            return sum(int_ceiled(len(v.outline), columns) for v in action.actions)
        elif isinstance(action, TagAction):
            return action.tag_type in (TagType.BR, TagType.SYMBOL)
        else:
            return int_ceiled(len(action.outline), columns)
    # NOTE: +2 is title pillar
    return sum(_in_action(v, columns) for v in scene.actions) + 2

def _acttypeCountsIn(story: Story, act_type: ActType):
    def _in_action(action: AllActions, act_type: ActType):
        if isinstance(action, CombAction):
            return sum(_in_action(v, act_type) for v in action.actions)
        elif isinstance(action, TagAction):
            return 0
        else:
            return action.act_type is act_type

    def _in_scene(scene: Scene, act_type: ActType):
        return sum(_in_action(v, act_type) for v in scene.actions)

    def _in_episode(episode: Episode, act_type: ActType):
        return sum(_in_scene(v, act_type) for v in episode.scenes)

    def _in_chapter(chapter: Chapter, act_type: ActType):
        return sum(_in_episode(v, act_type) for v in chapter.episodes)

    return sum(_in_chapter(v, act_type) for v in story.chapters)

def _descriptionManupaperCountsIn(story: Story, rows: int, columns: int) -> tuple:
    def _in_episode(episode: Episode, columns: int):
        return sum(_descriptionManupaperCountsInScene(v, columns) for v in episode.scenes)

    def _in_chapter(chapter: Chapter, columns: int):
        return sum(_in_episode(v, columns) for v in chapter.episodes)

    row_nums = sum(_in_chapter(v, columns) for v in story.chapters)
    papers = row_nums / rows
    return (papers, row_nums)

def _descriptionManupaperCountsInScene(scene: Scene, columns: int) -> int:
    def _in_action(action: AllActions, columns: int):
        if isinstance(action, CombAction):
            return sum(int_ceiled(len(strOfDescription(v)), columns) for v in action.actions)
        elif isinstance(action, TagAction):
            return action.tag_type in (TagType.BR, TagType.SYMBOL)
        else:
            return int_ceiled(len(strOfDescription(action)), columns)
    return sum(_in_action(v, columns) for v in scene.actions)

# math utility
def int_ceiled(a: [int, float], b: [int, float]) -> int:
    return -(-a // b)
