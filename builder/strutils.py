# -*- coding: utf-8 -*-
"""String utilities.
"""
import re
from . import assertion


# publics
def divided_by_splitter(target: str, splitter: str=','):
    tmp = target
    if splitter in target:
        return tuple(tmp.split(splitter))
    else:
        return tmp, tmp

def str_to_dict_by_splitter(target: [str, dict]) -> dict:
    if isinstance(target, dict):
        return target
    elif isinstance(target, str):
        if ":" in target:
            tmp = target.split(":")
            ret = {}
            for k, v in zip(tmp[0::2], tmp[1::2]):
                ret[k] = v
            return ret
        else:
            return {}

def str_replaced_tag_by_dictionary(target: str, words: dict, prefix: str="$") -> str:
    tmp = target
    for k, v in assertion.is_dict(words).items():
        if prefix in tmp:
            tmp = re.sub(r'\{}{}'.format(assertion.is_str(prefix), k), v, tmp)
        else:
            return tmp
    return tmp

def dict_sorted(origin: dict):
    return dict(sorted(origin.items(), key=lambda x:x[0]))

def str_duplicated_chopped(target: str):
    return re.sub(r'(。)+', r'\1',
            re.sub(r'(、)+', r'\1',
                re.sub(r'、。', r'、',
                    re.sub(r'([！？])[、。]', r'\1　',
                        assertion.is_str(target)))))

def extraspace_chopped(target: str) -> str:
    return re.sub(r'([、。」])[　](.)', r'\1\2', assertion.is_str(target))

def duplicate_bracket_chop_and_replaceed(target: str) -> str:
    return re.sub(r'」「', r'。', assertion.is_str(target))

