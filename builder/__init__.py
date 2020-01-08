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

__ASSET_ELEMENTS__ = (
        "PERSONS", "STAGES", "DAYS", "TIMES", "ITEMS", "WORDS", "RUBIS", "LAYERS",
        )

__FORMAT_DEFAULT__ = (0, 0, 0, 0)
__FORMAT_ESTAR__ = (1, 2, 2, 1)
__FORMAT_WEB__ = (0, 1, 1, 0)
__FORMAT_PHONE__ = (1, 1, 1, 1)

__DEF_YEAR__ = 2020
__DEF_MON__ = 1
__DEF_DAY__ = 1

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
    # talk action
    TALK = auto() # dialogue
    THINK = auto() # monologue
    EXPLAIN = auto() # status/narration
    VOICE = auto() # specific voice
    # other
    TAG = auto() # tag
    META = auto() # meta

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

class MetaType(Enum):
    NONE = auto()
    INFO = auto()
    TEST_EXISTS_THAT = auto()       # A subejct exists (in scene)
    TEST_HAS_THAT = auto()          # the subject has A item (object)

class TagType(Enum):
    NONE = auto()
    BR = auto() # break line
    COMMENT = auto() # comment
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

## named tuple
ConteData = namedtuple("ConteData",
        ("type", "dialogue", "subject", "objects", "content", "count", "note"))

History = namedtuple("History",
        ("date", "content", "note"))
