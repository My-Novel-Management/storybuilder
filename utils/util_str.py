# -*- coding: utf-8 -*-
"""Define utility for strings.
"""
## public libs
from typing import Tuple
import re
## local libs
from utils import assertion


## define re
RegAlpha = re.compile(r'^[a-zA-Z]+$')
RegKanji = re.compile("[一-龥]")


## public methods
def containsWordsIn(target: str, words: (str, list, tuple)) -> bool:
    if isinstance(words, str):
        return words in target
    else:
        for w in assertion.isList(words):
            if w and w in target:
                return True
        else:
            return False

def dictFromStrBySplitter(val: (str, dict), splitter: str) -> dict:
    if isinstance(val, dict):
        return val
    elif isinstance(val, str):
        if splitter in val:
            tmp = val.split(splitter)
            return dict([(k,v) for k,v in zip(tmp[0::2], tmp[1::2])])
        else:
            return {}
    else:
        AssertionError("cannot convert dict from str, mismatch type: {type(val)} of {val}")
        return {}

def isAlphabetsOnly(val: str) -> bool:
    return isinstance(val, str) and RegAlpha.match(val) is not None

def kanjiOf(target: str) -> list:
    return RegKanji.findall(assertion.isStr(target))

def strDividedBySplitter(val: str, splitter: str) -> Tuple[str, str]:
    return tuple(val.split(splitter)) if assertion.isStr(splitter) in assertion.isStr(val) else (val, val)

def strDuplicatedChopped(target: str):
    # NOTE:
    #   。。。　→　。
    #   、、、　→　、
    #   、。　　→　、
    #   ？、    →　？\u3000
    #   ！。    →　！\u3000
    return re.sub(r'(。)+', r'\1',
            re.sub(r'(、)+', r'\1',
                re.sub(r'、。', r'、',
                    re.sub(r'([!?！？])(.)', r'\1　\2',
                        re.sub(r'([!?！？])[、。]', r'\1　',
                            assertion.isStr(target))))))

def strReplacedTagByDict(target: str, tags: dict, prefix: str="$") -> str:
    tmp = assertion.isStr(target)
    for k, v in assertion.isDict(tags).items():
        if assertion.isStr(prefix) in tmp:
            tmp = re.sub(r'\{}{}'.format(prefix, k), v, tmp)
        else:
            return tmp
    return tmp

