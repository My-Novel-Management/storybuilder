# -*- coding: utf-8 -*-
__VERSION__ = "0.0.1"
__TITLE__ = "StoryBuilder"
__DESC__ = "Tool for building a story"


from enum import Enum, auto


## common values
__PRIORITY_NORMAL__ = 5
__PRIORITY_MAX__ = 10
__PRIORITY_MIN__ = 0

__PREFIX_STAGE__ = "on_"
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

## enums
class ActType(Enum):
    # exist control
    BE = auto() # put object in scene
    DESTROY = auto() # vanish object
    WEAR = auto() # put on object
    TAKEOFF = auto() # DESTROY wear
    HAVE = auto() # is-a object
    DISCARD = auto() # not is-a = DESTROY
    # object control
    MOVE = auto() # moving object
    COME = auto() # MOVE | BE
    GO = auto() # MOVE | DESTROY
    # effect
    HEAR = auto() # sound effect
    LOOK = auto() # paint object
    # basic action
    ACT = auto() # basic action
    THINK = auto() # monologue
    EXPLAIN = auto() # status
    # talk action
    TALK = auto() # dialogue
    # other
    TAG = auto() # tag

class TagType(Enum):
    NONE = auto()
    BR = auto() # break line
    COMMENT = auto() # comment
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
