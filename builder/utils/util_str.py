# -*- coding: utf-8 -*-
'''
Utility methods for strings
===========================
'''

__all__ = (
        'dict_from_string',
        'string_replaced_by_tag',
        'validate_dialogue_brackets',
        'validate_string_duplicate_chopped',
        )

from itertools import chain
from typing import Tuple
import re
from builder.utils import assertion


## define re
REG_ALPHA = re.compile(r'^[a-zA-Z]+$')
REG_KANJI = re.compile(r'[一-龥]')
REG_HIRAGANA = re.compile(r'[あ-ん]')
REG_KATAKANA = re.compile(r'[\u30A1-\u30FF]')


def dict_from_string(src: str, splitter: str) -> dict:
    ''' Convert a dictionary from a string.
    '''
    if assertion.is_str(splitter) in assertion.is_str(src):
        tmp = src.split(splitter)
        return dict([(k,v) for k,v in zip(tmp[0::2], tmp[1::2])])
    else:
        raise ValueError(f'Invalid string, cannot convert a dictionary: {src}')


def hiragana_list_from(src: str) -> list:
    ''' Get a hiragana list.
    '''
    return REG_HIRAGANA.findall(assertion.is_str(src))


def kanji_list_from(src: str) -> list:
    ''' Get a kanji list.
    '''
    return REG_KANJI.findall(assertion.is_str(src))


def katakana_list_from(src: str) -> list:
    ''' Get a katakana list.
    '''
    return REG_KATAKANA.findall(assertion.is_str(src))


def string_replaced_by_tag(src: str, tags: dict, prefix: str='$') -> str:
    ''' Replace the target word in a string by tags.
    '''
    tmp = assertion.is_str(src)
    for k, v in assertion.is_dict(tags).items():
        if assertion.is_str(prefix) in tmp:
            tmp = re.sub(r'\{}{}'.format(prefix, k), v, tmp)
        else:
            return tmp
    return tmp


def validate_dialogue_brackets(src: str) -> str:
    ''' Chop invalid brackets.
    '''
    return re.sub(r'』『', '。',
            re.sub(r'」「', '。',
                assertion.is_str(src)))


def validate_string_duplicate_chopped(src: str) -> str:
    ''' Chop a duplicated string end.

    NOTE:
        。。。 -> 。
        、、、 -> 、
        、。　 -> 、
        ？、　 -> ？\u3000
        ！。　 -> ！\u3000
    '''
    return re.sub(r'(。)+', r'\1',
            re.sub(r'(、)+', r'\1',
                re.sub(r'。、', r'。',
                re.sub(r'、。', r'、',
                    re.sub(r'([!?！？])\u3000[、。]', r'\1',
                    re.sub(r'([!?！？])([^ \u3000!?！？」』])', r'\1　\2',
                        re.sub(r'([!?！？])[、。]', r'\1　',
                            assertion.is_str(src))))))))

