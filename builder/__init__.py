# -*- coding: utf-8 -*-
__VERSION__ = "0.4.2"
__TITLE__ = "StoryBuilder"
__DESC__ = "Tool for building a story"


from collections import namedtuple
from enum import Enum, auto


## common values
__PRIORITY_NORMAL__ = 5
__PRIORITY_MAX__ = 10
__PRIORITY_MIN__ = 0

__PREFIX_STAGE__ = "on_"
__SUFFIX_STAGE_INT__ = "_int"
__SUFFIX_STAGE_EXT__ = "_ext"
__PREFIX_DAY__ = "in_"
__PREFIX_TIME__ = "at_"
__PREFIX_WORD__ = "w_"


__MECAB_LINUX1__ = "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd"
__MECAB_LINUX2__ = "-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"

__TAG_PREFIX__ = "$"

__BASE_COLUMN__ = 20
__BASE_ROW__ = 20

__DEF_FILENAME__ = "story"

__CONTINUED__ = "__continued__"

__ASSET_ELEMENTS__ = (
        "PERSONS", "AREAS", "STAGES", "DAYS", "TIMES", "ITEMS", "WORDS", "RUBIS", "LAYERS",
        )

__FORMAT_DEFAULT__ = (0, 0, 0, 0)
__FORMAT_ESTAR__ = (1, 2, 2, 1)
__FORMAT_WEB__ = (0, 1, 1, 0)
__FORMAT_PHONE__ = (1, 1, 1, 1)

__DEF_YEAR__ = 2020
__DEF_MON__ = 1
__DEF_DAY__ = 1

__WALK_STAGE__ = [
        "路地", "路上",
        "歩道",
        "交差点", "横断歩道",
        "山道",
        "街道",
        ]
__DRIVE_STAGE__ = [
        "車", "車・内",
        "バス", "バス・内",
        "タクシー", "タクシー・内",
        "電車", "電車・内",
        "列車", "列車・内",
        "新幹線", "新幹線・内",
        "自転車",
        "バイク",
        "船", "船・内",
        "フェリー", "フェリー・内",
        "飛行機", "飛行機・内",
        "自家用ジェット", "自家用ジェット・内",
        "ヘリコプター", "ヘリコプター・内",
        ]

## enums
class ActType(Enum):
    # basic action
    ACT = auto() # basic action
    # object control
    BE = auto() # put object in scene
    DESTROY = auto() # vanish object
    HAVE = auto() # is-a object
    DISCARD = auto() # not is-a = DESTROY
    COME = auto()
    GO = auto()
    # effect
    HEAR = auto() # sound effect
    LOOK = auto() # paint object
    WEAR = auto() # put texture
    # talk action
    TALK = auto() # dialogue
    THINK = auto() # monologue
    EXPLAIN = auto() # status/narration
    VOICE = auto() # specific voice
    # other
    TAG = auto() # tag
    META = auto() # meta

    def emoji(self) -> str:
        return {
                ActType.ACT: "↓",
                ActType.BE: "∃",
                ActType.COME: "→",
                ActType.DESTROY: "壊",
                ActType.DISCARD: "捨",
                ActType.EXPLAIN: "※",
                ActType.GO: "←",
                ActType.HAVE: "∈",
                ActType.HEAR: "♪",
                ActType.LOOK: "■",
                ActType.META: "∇",
                ActType.TAG: "🔖",
                ActType.TALK: "💬",
                ActType.THINK: "😌",
                ActType.VOICE: "📞",
                ActType.WEAR: "👕",
                }[self]

class DataType(Enum):
    NONE = auto()
    ACTION = auto() # action
    HEAD = auto() # sceneより上位のcontainer
    TITLE = auto() # title
    DATA_STR = auto()
    DATA_LIST = auto()
    DATA_DICT = auto()
    STORY_TITLE = auto()
    CHAPTER_TITLE = auto()
    EPISODE_TITLE = auto()
    SCENE_TITLE = auto()
    SCENE_SETTING = auto()
    STAGE_SETTING = auto()
    PERSON_SETTING = auto()
    SCENE_OBJECT = auto()
    TAG = auto()
    DESCRIPTION = auto()
    DIALOGUE = auto()
    MONOLOGUE = auto()
    NARRATION = auto()
    VOICE = auto()
    META = auto()
    COMMAND = auto() # 特殊なもので利用。方式の切り替え等

class MetaType(Enum):
    NONE = auto()
    INFO = auto()
    TEST_EXISTS_THAT = auto()       # A subejct exists (in scene)
    TEST_HAS_THAT = auto()          # the subject has A item (object)
    BLOCK_START = auto()
    BLOCK_END = auto()
    EVENT_START = auto()
    EVENT_POINT = auto()
    EVENT_END = auto()

class TagType(Enum):
    NONE = auto()
    BR = auto() # break line
    COMMENT = auto() # comment
    COMMAND = auto() # special command
    OUTLINE = auto() # outline
    HR = auto() # horizontal line
    SYMBOL = auto() # symbol mark
    TITLE = auto() # title

class WordClasses(Enum):
    NOUN = "名詞"
    VERB = "動詞"
    ADJECTIVE = "形容詞"
    ADVERB = "副詞"
    CONJUCTION = "接続詞"
    INTERJECTION = "感動詞"
    AUXVERB = "助動詞"
    PARTICLE = "助詞"
    MARK = "記号"
    PREFIX = "接頭詞"
    OTHER = "その他"

    def convVolume(self) -> int:
        return {
                WordClasses.ADJECTIVE: 1,
                WordClasses.ADVERB: 1,
                WordClasses.AUXVERB: 0,
                WordClasses.CONJUCTION: 0,
                WordClasses.INTERJECTION: 1,
                WordClasses.MARK: 0,
                WordClasses.NOUN: 10,
                WordClasses.OTHER: 0,
                WordClasses.PARTICLE: 0,
                WordClasses.PREFIX: 0,
                WordClasses.VERB: 3,
                }[self]

## named tuple
ConteData = namedtuple("ConteData",
        ("type", "dialogue", "subject", "objects", "content", "count", "note"))

History = namedtuple("History",
        ("date", "content", "note"))
