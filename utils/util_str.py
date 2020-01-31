# -*- coding: utf-8 -*-
"""Define utility for strings.
"""
## public libs
from itertools import chain
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

def daytimeDictSorted(origin: dict, is_reverse: bool=True) -> dict:
    inversed = dict([(v.data,k) for k,v in origin.items()])
    tmp = dictSorted(inversed, is_reverse)
    res = []
    for key in tmp.values():
        for k,v in origin.items():
            if k == key:
                res.append((k,v))
    return dict(res)

def dictCombined(a: dict, b: dict) -> dict:
    return {**a, **b}

def dictSorted(origin: dict, is_reverse: bool=True) -> dict:
    return dict(sorted(origin.items(), key=lambda x:x[0], reverse=is_reverse))

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

def hanToZen(val: str) -> str:
    return val.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))

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
                re.sub(r'。、', r'。',
                re.sub(r'、。', r'、',
                    re.sub(r'([!?！？])\u3000[、。]', r'\1',
                    re.sub(r'([!?！？])([^ \u3000!?！？」』])', r'\1　\2',
                        re.sub(r'([!?！？])[、。]', r'\1　',
                            assertion.isStr(target))))))))

def strEllipsis(val: str, width: int, placeholder: str="…") -> str:
    return val[0:width - 1] + placeholder if len(val) >= width else val

def strJoinIf(vals: (list, tuple), separator: str="") -> str:
    if vals:
        return separator.join(vals)
    else:
        return ""

def strReplacedTagByDict(target: str, tags: dict, prefix: str="$") -> str:
    tmp = assertion.isStr(target)
    for k, v in assertion.isDict(tags).items():
        if assertion.isStr(prefix) in tmp:
            tmp = re.sub(r'\{}{}'.format(prefix, k), v, tmp)
        else:
            return tmp
    return tmp

def tupleEvenStr(val: (str, list, tuple)) -> tuple:
    if not val:
        return ()
    elif isinstance(val, str):
        return (val,)
    elif isinstance(val, (tuple, list)):
        if isinstance(val[0], (tuple, list)):
            return tuple(chain.from_iterable(val))
        else:
            return val if isinstance(val, tuple) else tuple(val)
    else:
        assert isinstance(val, (str, list, tuple))
        return ()

def tupleFiltered(origin: (list, tuple), filter_type: (object, tuple)) -> tuple:
    return tuple(v for v in origin if isinstance(v, filter_type))
