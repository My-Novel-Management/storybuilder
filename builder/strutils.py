# -*- coding: utf-8 -*-
"""String utilities.
"""
import re
from . import assertion


# publics
def dict_sorted(origin: dict) -> dict:
    return dict(sorted(origin.items(), key=lambda x:x[0]))

def divided_by_splitter(target: str, splitter: str=',') -> tuple:
    return tuple(target.split(splitter)) if assertion.is_str(splitter) in assertion.is_str(target) else (target, target)

def duplicate_bracket_chop_and_replaceed(target: str) -> str:
    return re.sub(r'」「', r'。', assertion.is_str(target))

def extraspace_chopped(target: str) -> str:
    return re.sub(r'([、。」])[　](.)', r'\1\2', assertion.is_str(target))

def str_duplicated_chopped(target: str):
    # NOTE:
    #   。。。　→　。
    #   、、、　→　、
    #   、。　　→　、
    #   ？、    →　？\u3000
    #   ！。    →　！\u3000
    return re.sub(r'(。)+', r'\1',
            re.sub(r'(、)+', r'\1',
                re.sub(r'、。', r'、',
                    re.sub(r'([!?！？])[、。]', r'\1　',
                        assertion.is_str(target)))))

def str_replaced_tag_by_dictionary(target: str, words: dict, prefix: str="$") -> str:
    tmp = assertion.is_str(target)
    for k, v in assertion.is_dict(words).items():
        if assertion.is_str(prefix) in tmp:
            tmp = re.sub(r'\{}{}'.format(prefix, k), v, tmp)
        else:
            return tmp
    return tmp

def str_to_dict_by_splitter(target: [str, dict]) -> dict:
    if isinstance(target, dict):
        return target
    elif isinstance(target, str):
        if ":" in target:
            tmp = target.split(":")
            return dict([(k,v) for k,v in zip(tmp[0::2], tmp[1::2])])
        else:
            return {}
    else:
        raise TypeError(f"value type is mismatch!!: {type(target)}")

