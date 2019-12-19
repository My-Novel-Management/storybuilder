# -*- coding: utf-8 -*-
"""The analyze tool.
"""
import re
from collections import Counter
from itertools import chain
import MeCab
from . import assertion
from .action import Action, ActType, TagAction, TagType
from .basesubject import NoSubject
from .chapter import Chapter
from .chara import Chara
from .combaction import CombAction
from .description import Description, DescType, NoDesc
from .episode import Episode
from .flag import Flag, NoFlag, NoDeflag
from .parser import Parser
from .person import Person
from .scene import Scene
from .story import Story
from .utils import strOfDescription, toSomething, hasTrueList, isDialogue, personsSorted, flagsSorted


## define type
AllActions = (Action, CombAction, TagAction)
BaseActions = (Action, TagAction)
TargetPerson = (Person, Chara, NoSubject)
AllFlags = (Flag, NoFlag, NoDeflag)
StoryContainers = (Story, Chapter, Episode, Scene)


class Analyzer(object):
    """The story analyze tools.
    """
    DEF_BASEMENT = 10
    DEF_BASEROWS = 20
    DEF_BASECOLUMNS = 20

    def __init__(self, dic: str):
        self.tokenizer = MeCab.Tagger(dic)
        self.src = None
        # NOTE: mecab hack
        self.tokenizer.parse('')

    ## base analyzing
    def actionsCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_actionsCountIn,
                chapterFnc=_actionsCountInChapter,
                episodeFnc=_actionsCountInEpisode,
                sceneFnc=_actionsCountInScene,
                src=src)

    def acttypeCount(self, src: StoryContainers, act_type: ActType) -> int:
        return toSomething(self,
                act_type,
                storyFnc=_acttypeCountIn,
                chapterFnc=_acttypeCountInChapter,
                episodeFnc=_acttypeCountInEpisode,
                sceneFnc=_acttypeCountInScene,
                src=src)

    def actTypesCountsFrom(self, src: StoryContainers) -> dict:
        return dict([(v, self.acttypeCount(src, v)) for v in ActType])

    def chaptersCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_chaptersCountIn,
                chapterFnc=_chaptersCountInChapter,
                episodeFnc=_chaptersCountInEpisode,
                sceneFnc=_chaptersCountInScene,
                src=src)

    def descsContainsWord(self, src: StoryContainers, word: str) -> bool:
        return toSomething(self,
                word,
                storyFnc=_descriptionContainsWordIn,
                chapterFnc=_descriptionContainsWordInChapter,
                episodeFnc=_descriptionContainsWordInEpisode,
                sceneFnc=_descriptionContainsWordInScene,
                src=src)

    def descsManupaperRowCount(self, src: StoryContainers, columns: int) -> int:
        return toSomething(self,
                columns,
                storyFnc=_descsManupaperRowCountIn,
                chapterFnc=_descsManupaperRowCountInChapter,
                episodeFnc=_descsManupaperRowCountInEpisode,
                sceneFnc=_descsManupaperRowCountInScene,
                src=src)

    def descriptionsCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_descsCountIn,
                chapterFnc=_descsCountInChapter,
                episodeFnc=_descsCountInEpisode,
                sceneFnc=_descsCountInScene,
                src=src)

    def dialoguesCount(self, src: StoryContainers, person: Person) -> int:
        return toSomething(self,
                person,
                storyFnc=_dialoguesCountIn,
                chapterFnc=_dialoguesCountInChapter,
                episodeFnc=_dialoguesCountInEpisode,
                sceneFnc=_dialoguesCountInScene,
                src=src)

    def dialoguesOfPerson(self, src: StoryContainers, person: Person) -> list:
        return toSomething(self,
                person,
                storyFnc=_dialoguesOfPersonIn,
                chapterFnc=_dialoguesOfPersonInChapter,
                episodeFnc=_dialoguesOfPersonInEpisode,
                sceneFnc=_dialoguesOfPersonInScene,
                src=src)

    def episodesCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_episodesCountIn,
                chapterFnc=_episodesCountInChapter,
                episodeFnc=_episodesCountInEpisode,
                sceneFnc=_episodesCountInScene,
                src=src)

    def flagsCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_flagsCountIn,
                chapterFnc=_flagsCountInChapter,
                episodeFnc=_flagsCountInEpisode,
                sceneFnc=_flagsCountInScene,
                src=src)

    def flagsFrom(self, src: StoryContainers) -> list:
        return flagsSorted(list(set(toSomething(self,
                storyFnc=_flagsFromIn,
                chapterFnc=_flagsFromInChapter,
                episodeFnc=_flagsFromInEpisode,
                sceneFnc=_flagsFromInScene,
                src=src))))

    def generateGramPartWordsCount(self, src: StoryContainers, gram: str,
            subinfo: str="") -> Counter:
        return Counter(
                toSomething(self,
                    self, gram, subinfo,
                    storyFnc=_genGramPartWordsIn,
                    chapterFnc=_genGramPartWordsInChapter,
                    episodeFnc=_genGramPartWordsInEpisode,
                    sceneFnc=_genGramPartWordsInScene,
                    src=src,
                ))

    def outlineContainsWord(self, src: StoryContainers, word: str) -> bool:
        return toSomething(self,
                word,
                storyFnc=_outlineContainsWordIn,
                chapterFnc=_outlineContainsWordInChapter,
                episodeFnc=_outlineContainsWordInEpisode,
                sceneFnc=_outlineContainsWordInScene,
                src=src)

    def outlinesCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_outlinesCountIn,
                chapterFnc=_outlinesCountInChapter,
                episodeFnc=_outlinesCountInEpisode,
                sceneFnc=_outlinesCountInScene,
                src=src)

    def outlinesManupaperRowCount(self, src: StoryContainers, columns: int) -> int:
        return toSomething(self,
                columns,
                storyFnc=_outlinesManupaperRowCountIn,
                chapterFnc=_outlinesManupaperRowCountInChapter,
                episodeFnc=_outlinesManupaperRowCountInEpisode,
                sceneFnc=_outlinesManupaperRowCountInScene,
                src=src)

    def personsFrom(self, src: StoryContainers) -> list:
        return personsSorted(list(set(toSomething(self,
                storyFnc=_personsFromIn,
                chapterFnc=_personsFromInChapter,
                episodeFnc=_personsFromInEpisode,
                sceneFnc=_personsFromInScene,
                src=src))))

    def scenesCount(self, src: StoryContainers) -> int:
        return toSomething(self,
                storyFnc=_scenesCountIn,
                chapterFnc=_scenesCountInChapter,
                episodeFnc=_scenesCountInEpisode,
                sceneFnc=_scenesCountInScene,
                src=src)

    ## utility analyzing
    def actionsPercent(self, src: StoryContainers) -> dict:
        acttypes = self.actTypesCountsFrom(src)
        total = sum(v for v in acttypes.values())
        def _percent(v):
            return acttypes[v] / total * 100 if total else 0
        return dict([(v.name.capitalize(), _percent(v)) for v in ActType])

    def charactersCount(self, src: StoryContainers,
            columns: int=DEF_BASECOLUMNS, rows: int=DEF_BASEROWS) -> dict:
        return {"desc_total": self.descriptionsCount(src),
                "outline_total": self.outlinesCount(src),
                "estimated": self.descsEstimatedCount(src),
                "desc_rows": self.descsManupaperRowCount(src, columns),
                "outline_rows": self.outlinesManupaperRowCount(src, columns),
                "base_columns": columns,
                "base_rows": rows,
                }

    def charactersCountEachScenes(self, story: Story,
            columns: int=DEF_BASECOLUMNS, rows: int=DEF_BASEROWS) -> list:
        tmp = []
        ch_num, ep_num, sc_num = 1, 1, 1
        for ch in story.chapters:
            tmp.append((f"Ch-{ch_num}: {ch.title}",
                self.charactersCount(ch, columns, rows)))
            ch_num += 1
            for ep in ch.episodes:
                tmp.append((f"Ep-{ep_num}: {ep.title}",
                    self.charactersCount(ep, columns, rows)))
                ep_num += 1
                for sc in ep.scenes:
                    tmp.append((f"Sc-1{sc_num}: {sc.title}",
                        self.charactersCount(sc, columns, rows)))
                    sc_num += 1
        return tmp

    def containsWord(self, src: StoryContainers, words: (str, list, tuple),
            useAnd: bool=True) -> bool:
        '''Check the word to contain the source.
        '''
        if isinstance(words, str):
            return self.outlineContainsWord(src, words) or self.descsContainsWord(src, words)
        else:
            assertion.is_list(words)
            if useAnd:
                return not hasTrueList(
                        words,
                        lambda v, src: not (self.outlineContainsWord(src, v) or self.descsContainsWord(src, v)),
                        src)
            else:
                return hasTrueList(
                        words,
                        lambda v, src: (self.outlineContainsWord(src, v) or self.descsContainsWord(src, v)),
                        src)

    def descsEstimatedCount(self, src: StoryContainers, basement: int=DEF_BASEMENT) -> int:
        tmp = self.actTypesCountsFrom(src)
        def multi(t, v):
            if t is ActType.BE: return v * 1
            elif t in (ActType.GO, ActType.COME): return v * 2
            elif t is ActType.TAG: return v * 0
            else: return v * 4
        return sum([multi(k, v) for k,v in tmp.items()]) * basement

    def dialoguesEachPerson(self, src: StoryContainers) -> list:
        tmp = []
        persons = self.personsFrom(src)
        for v in persons:
            t = self.dialoguesOfPerson(src,v)
            tmp.append((v.name, self.dialoguesOfPerson(src, v)))
        return tmp

    # main analyzing methods
    def frequency_words(self, story: Story):
        # TODO: all story source
        is_comment = False
        descs = Parser(story).toDescriptions(False)
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

## privates (detail)
### counts
'''Action counts
'''
def _actionsCountIn(story: Story) -> int:
    return sum(_actionsCountInChapter(v) for v in story.chapters)

def _actionsCountInChapter(chapter: Chapter) -> int:
    return sum(_actionsCountInEpisode(v) for v in chapter.episodes)

def _actionsCountInEpisode(episode: Episode) -> int:
    return sum(_actionsCountInScene(v) for v in episode.scenes)

def _actionsCountInScene(scene: Scene) -> int:
    return sum(_actionsCountInAction(v) for v in scene.actions)

def _actionsCountInAction(action: AllActions) -> int:
    if isinstance(action, CombAction):
        return sum(_actionsCountInAction(v) for v in action.actions)
    else:
        return 1

'''Act type count
'''
def _acttypeCountIn(story: Story, act_type: ActType) -> int:
    return sum(_acttypeCountInChapter(v, act_type) for v in story.chapters)

def _acttypeCountInChapter(chapter: Chapter, act_type: ActType) -> int:
    return sum(_acttypeCountInEpisode(v, act_type) for v in chapter.episodes)

def _acttypeCountInEpisode(episode: Episode, act_type: ActType) -> int:
    return sum(_acttypeCountInScene(v, act_type) for v in episode.scenes)

def _acttypeCountInScene(scene: Scene, act_type: ActType) -> int:
    return sum(_acttypeCountInAction(v, act_type) for v in scene.actions)

def _acttypeCountInAction(action: AllActions, act_type: ActType) -> int:
    if isinstance(action, CombAction):
        return sum(_acttypeCountInAction(v, act_type) for v in action.actions)
    elif isinstance(action, TagAction):
        return action.act_type == act_type
    else:
        return action.act_type == act_type

'''chapters count
'''
def _chaptersCountIn(story: Story) -> int:
    return sum(_chaptersCountInChapter(v) for v in story.chapters)

def _chaptersCountInChapter(chapter: Chapter) -> int:
    return 1

def _chaptersCountInEpisode(episode: Episode) -> int:
    return 0

def _chaptersCountInScene(scene: Scene) -> int:
    return 0

'''descriptions count
'''
def _descsCountIn(story: Story) -> int:
    return sum(_descsCountInChapter(v) for v in story.chapters)

def _descsCountInChapter(chapter: Chapter) -> int:
    return sum(_descsCountInEpisode(v) for v in chapter.episodes)

def _descsCountInEpisode(episode: Episode) -> int:
    return sum(_descsCountInScene(v) for v in episode.scenes)

def _descsCountInScene(scene: Scene) -> int:
    return sum(_descsCountInAction(v) for v in scene.actions)

def _descsCountInAction(action: AllActions) -> int:
    if isinstance(action, CombAction):
        return sum(_descsCountInAction(v) for v in action.actions)
    elif isinstance(action, TagAction):
        return 0
    else:
        return _descsCountOfAction(action)

def _descsCountOfAction(action: Action) -> int:
    tmp = len(strOfDescription(action))
    if tmp:
        return tmp + 2 if isDialogue(action) else tmp + 1
    else:
        return 0

'''description manupaper row count
'''
def _descsManupaperRowCountIn(story: Story, columns: int) -> int:
    return sum(_descsManupaperRowCountInChapter(v, columns) for v in story.chapters)

def _descsManupaperRowCountInChapter(chapter: Chapter, columns: int) -> int:
    return sum(_descsManupaperRowCountInEpisode(v, columns) for v in chapter.episodes)

def _descsManupaperRowCountInEpisode(episode: Episode, columns: int) -> int:
    return sum(_descsManupaperRowCountInScene(v, columns) for v in episode.scenes)

def _descsManupaperRowCountInScene(scene: Scene, columns: int) -> int:
    return sum(_descsManupaperRowCountInAction(v, columns) for v in scene.actions)

def _descsManupaperRowCountInAction(action: AllActions, columns: int) -> int:
    if isinstance(action, CombAction):
        return sum(int_ceiled(_descsCountOfAction(v), columns) for v in action.actions)
    elif isinstance(action, TagAction):
        return action.tag_type is (TagType.BR, TagType.SYMBOL)
    else:
        return int_ceiled(_descsCountOfAction(action), columns)

'''dialogue count
'''
def _dialoguesCountIn(story: Story, person: Person) -> int:
    return sum(_dialoguesCountInChapter(v, person) for v in story.chapters)

def _dialoguesCountInChapter(chapter: Chapter, person: Person) -> int:
    return sum(_dialoguesCountInEpisode(v, person) for v in chapter.episodes)

def _dialoguesCountInEpisode(episode: Episode, person: Person) -> int:
    return sum(_dialoguesCountInScene(v, person) for v in episode.scenes)

def _dialoguesCountInScene(scene: Scene, person: Person) -> int:
    return sum(_dialoguesCountInAction(v, person) for v in scene.actions)

def _dialoguesCountInAction(action: AllActions, person: Person) -> int:
    if isinstance(action, CombAction):
        return sum(_dialoguesCountInAction(v, person) for v in action.actions)
    elif isinstance(action, TagAction):
        return 0
    else:
        return isDialogue(action) \
                and isinstance(action.subject, Person) and action.subject.equals(person)

'''episodes count
'''
def _episodesCountIn(story: Story) -> int:
    return sum(_episodesCountInChapter(v) for v in story.chapters)

def _episodesCountInChapter(chapter: Chapter) -> int:
    return sum(_episodesCountInEpisode(v) for v in chapter.episodes)

def _episodesCountInEpisode(episode: Episode) -> int:
    return 1

def _episodesCountInScene(scene: Scene) -> int:
    return 0

'''flags count
'''
def _flagsCountIn(story: Story) -> int:
    return sum(_flagsCountInChapter(v) for v in story.chapters)

def _flagsCountInChapter(chapter: Chapter) -> int:
    return sum(_flagsCountInEpisode(v) for v in chapter.episodes)

def _flagsCountInEpisode(episode: Episode) -> int:
    return sum(_flagsCountInScene(v) for v in episode.scenes)

def _flagsCountInScene(scene: Scene) -> int:
    return sum(_flagsCountInAction(v) for v in scene.actions)

def _flagsCountInAction(action: AllActions) -> int:
    if isinstance(action, CombAction):
        return sum(_flagsCountInAction(v) for v in action.actions)
    elif isinstance(action, TagAction):
        return 0
    else:
        return len([v for v in (action.getFlag(), action.getDeflag()) if not isinstance(v, (NoFlag, NoDeflag))])

'''outlines count
'''
def _outlinesCountIn(story: Story) -> int:
    return sum(_outlinesCountInChapter(v) for v in story.chapters)

def _outlinesCountInChapter(chapter: Chapter) -> int:
    return sum(_outlinesCountInEpisode(v) for v in chapter.episodes)

def _outlinesCountInEpisode(episode: Episode) -> int:
    return sum(_outlinesCountInScene(v) for v in episode.scenes)

def _outlinesCountInScene(scene: Scene) -> int:
    return sum(_outlinesCountInAction(v) for v in scene.actions)

def _outlinesCountInAction(action: AllActions) -> int:
    if isinstance(action, CombAction):
        return sum(_outlinesCountInAction(v) for v in action.actions)
    elif isinstance(action, TagAction):
        return 0
    else:
        return len(action.outline)

'''outlines manupaper row count
'''
def _outlinesManupaperRowCountIn(story: Story, columns: int) -> int:
    return sum(_outlinesManupaperRowCountInChapter(v, columns) for v in story.chapters)

def _outlinesManupaperRowCountInChapter(chapter: Chapter, columns: int) -> int:
    return sum(_outlinesManupaperRowCountInEpisode(v, columns) for v in chapter.episodes)

def _outlinesManupaperRowCountInEpisode(episode: Episode, columns: int) -> int:
    return sum(_outlinesManupaperRowCountInScene(v, columns) for v in episode.scenes)

def _outlinesManupaperRowCountInScene(scene: Scene, columns: int) -> int:
    return sum(_outlinesManupaperRowCountInAction(v, columns) for v in scene.actions)

def _outlinesManupaperRowCountInAction(action: AllActions, columns: int) -> int:
    if isinstance(action, CombAction):
        return sum(int_ceiled(len(v.outline), columns) for v in action.actions)
    elif isinstance(action, TagAction):
        return action.tag_type in (TagType.BR, TagType.SYMBOL)
    else:
        return int_ceiled(len(action.outline), columns)

'''scenes count
'''
def _scenesCountIn(story: Story) -> int:
    return sum(_scenesCountInChapter(v) for v in story.chapters)

def _scenesCountInChapter(chapter: Chapter) -> int:
    return sum(_scenesCountInEpisode(v) for v in chapter.episodes)

def _scenesCountInEpisode(episode: Episode) -> int:
    return sum(_scenesCountInScene(v) for v in episode.scenes)

def _scenesCountInScene(scene: Scene) -> int:
    return 1

### contains
'''description contains word
'''
def _descriptionContainsWordIn(story: Story, word: str) -> bool:
    return hasTrueList(story.chapters, _descriptionContainsWordInChapter, word)

def _descriptionContainsWordInChapter(chapter: Chapter, word: str) -> bool:
    return hasTrueList(chapter.episodes, _descriptionContainsWordInEpisode, word)

def _descriptionContainsWordInEpisode(episode: Episode, word: str) -> bool:
    return hasTrueList(episode.scenes, _descriptionContainsWordInScene, word)

def _descriptionContainsWordInScene(scene: Scene, word: str) -> bool:
    return hasTrueList(scene.actions, _descriptionContainsWordInAction, word)

def _descriptionContainsWordInAction(action: AllActions, word: str) -> bool:
    if isinstance(action, CombAction):
        return hasTrueList(action.actions, _descriptionContainsWordInAction, word)
    elif isinstance(action, TagAction):
        return False
    else:
        return word in strOfDescription(action)

'''outline contains word
'''
def _outlineContainsWordIn(story: Story, word: str) -> bool:
    return hasTrueList(story.chapters, _outlineContainsWordInChapter, word)

def _outlineContainsWordInChapter(chapter: Chapter, word: str) -> bool:
    return hasTrueList(chapter.episodes, _outlineContainsWordInEpisode, word)

def _outlineContainsWordInEpisode(episode: Episode, word: str) -> bool:
    return hasTrueList(episode.scenes, _outlineContainsWordInScene, word)

def _outlineContainsWordInScene(scene: Scene, word: str) -> bool:
    return hasTrueList(scene.actions, _outlineContainsWordInAction, word)

def _outlineContainsWordInAction(action: AllActions, word: str) -> bool:
    if isinstance(action, CombAction):
        return hasTrueList(action.actions, _outlineContainsWordInAction, word)
    elif isinstance(action, TagAction):
        return False
    else:
        return word in action.outline

## convert


## extractor
def _dialoguesOfPersonIn(story: Story, person: Person) -> list:
    return list(chain.from_iterable(_dialoguesOfPersonInChapter(v, person) for v in story.chapters))

def _dialoguesOfPersonInChapter(chapter: Chapter, person: Person) -> list:
    return list(chain.from_iterable(_dialoguesOfPersonInEpisode(v, person) for v in chapter.episodes))

def _dialoguesOfPersonInEpisode(episode: Episode, person: Person) -> list:
    return list(chain.from_iterable(_dialoguesOfPersonInScene(v, person) for v in episode.scenes))

def _dialoguesOfPersonInScene(scene: Scene, person: Person) -> list:
    return list(chain.from_iterable(_dialoguesOfPersonInAction(v, person) for v in scene.actions))

def _dialoguesOfPersonInAction(action: AllActions, person: Person) -> list:
    def _exceptNoDesc(act: Action):
        if isinstance(act.description, NoDesc):
            return ""
        else:
            return strOfDescription(act)
    if isinstance(action, CombAction):
        return list(chain.from_iterable(_dialoguesOfPersonInAction(v, person) for v in action.actions))
    elif isinstance(action, TagAction):
        return []
    else:
        return [_exceptNoDesc(action)] if (isDialogue(action) and isinstance(action.subject, Person) and action.subject.equals(person)) else []

'''flags list from
'''
def _flagsFromIn(story: Story) -> list:
    return list(chain.from_iterable(_flagsFromInChapter(v) for v in story.chapters))

def _flagsFromInChapter(chapter: Chapter) -> list:
    return list(chain.from_iterable(_flagsFromInEpisode(v) for v in chapter.episodes))

def _flagsFromInEpisode(episode: Episode) -> list:
    return list(chain.from_iterable(_flagsFromInScene(v) for v in episode.scenes))

def _flagsFromInScene(scene: Scene) -> list:
    return list(chain.from_iterable(_flagsFromInAction(v) for v in scene.actions))

def _flagsFromInAction(action: AllActions) -> list:
    if isinstance(action, CombAction):
        return list(chain.from_iterable(_flagsFromInAction(v) for v in action.actions))
    elif isinstance(action, TagAction):
        return []
    else:
        return [action.getFlag(), action.getDeflag()]

'''persons list from
'''
def _personsFromIn(story: Story) -> list:
    return list(chain.from_iterable(_personsFromInChapter(v) for v in story.chapters))

def _personsFromInChapter(chapter: Chapter) -> list:
    return list(chain.from_iterable(_personsFromInEpisode(v) for v in chapter.episodes))

def _personsFromInEpisode(episode: Episode) -> list:
    return list(chain.from_iterable(_personsFromInScene(v) for v in episode.scenes))

def _personsFromInScene(scene: Scene) -> list:
    return list(chain.from_iterable(_personsFromInAction(v) for v in scene.actions))

def _personsFromInAction(action: AllActions) -> list:
    if isinstance(action, CombAction):
        return list(chain.from_iterable(_personsFromInAction(v) for v in action.actions))
    elif isinstance(action, TagAction):
        return []
    else:
        return [action.subject] if isinstance(action.subject, Person) else []

## generate
def _genGramPartWordsIn(story: Story, az: Analyzer, gram: str, subinfo: str) -> list:
    return list(chain.from_iterable([_genGramPartWordsInChapter(v, az, gram, subinfo) for v in story.chapters]))

def _genGramPartWordsInChapter(chapter: Chapter, az: Analyzer, gram: str, subinfo: str) -> list:
    return list(chain.from_iterable([_genGramPartWordsInEpisode(v, az, gram, subinfo) for v in chapter.episodes]))

def _genGramPartWordsInEpisode(episode: Episode, az: Analyzer, gram: str, subinfo: str) -> list:
    return list(chain.from_iterable([_genGramPartWordsInScene(v, az, gram, subinfo) for v in episode.scenes]))

def _genGramPartWordsInScene(scene: Scene, az: Analyzer, gram: str, subinfo: str) -> list:
    return list(chain.from_iterable([_genGramPartWordsInAction(v, az, gram, subinfo) for v in scene.actions]))

def _genGramPartWordsInAction(action: AllActions, az: Analyzer, gram: str,
        subinfo: str) -> list:
    if isinstance(action, CombAction):
        return list(chain.from_iterable([_genGramPartWordsInAction(v, az, gram, subinfo) for v in action.actions]))
    elif isinstance(action, TagAction):
        return []
    else:
        def _except(t: str):
            return t in ('EOS', '', 't', 'ー')
        parsed = az.tokenizer.parse(strOfDescription(action)).split("\n")
        tokens = (re.split('[\t,]', v) for v in parsed)
        def _ifcond(v, gram, subinfo):
            if v and not _except(v[0]):
                if v[1] == gram:
                    return subinfo in (v[2], v[3]) if subinfo else True
            return False
        tmp = [v[0] for v in tokens if _ifcond(v, gram, subinfo)]
        return tmp

## math utility
def int_ceiled(a: [int, float], b: [int, float]) -> int:
    return -(-assertion.is_int(a) // assertion.is_int(b))
