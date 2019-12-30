# -*- coding: utf-8 -*-
"""Define tool for analyze
"""
## public libs
from collections import Counter
import re
from typing import Dict
## third party libs
import MeCab
## local libs
from utils import assertion
## local files
from builder import WordClasses
from builder.action import Action
from builder.chapter import Chapter
from builder.episode import Episode
from builder.extractor import Extractor
from builder.scene import Scene
from builder.shot import Shot
from builder.story import Story


## define types
StoryLike = (Story, Chapter, Episode, Scene)


class Analyzer(object):
    """The tool class for analyze
    """
    def __init__(self, mecabdir: str):
        self.tokenizer = MeCab.Tagger(mecabdir)
        ## NOTE:
        ##  必要な初期化
        self.tokenizer.parse('')

    ## methos
    def collectionsWordClassByMecab(self, src: StoryLike) -> Dict[str, list]:
        '''
            - 名詞
            - 動詞
            - 形容詞
            - 副詞
            - 接続詞
            - 感動詞
            - 助動詞
            - 助詞
            - 記号
            - 接頭詞
            - その他（フィラー）
        '''
        nouns, verbs, adjectives, adverbs = [], [], [], []
        conjuctions, interjections, auxverbs, particles = [], [], [], []
        marks, prefixs, others = [], [], []
        extr = Extractor(src)
        tmp = []
        def _excepted(target: str):
            return target in ('EOS', '', 't', 'ー')
        for info in [v.infos for v in extr.shots]:
            for v in info:
                tmp.append(v)
        parsed = self.tokenizer.parse("\n".join(tmp)).split("\n")
        tokens = (re.split('[\t,]', v) for v in parsed)
        for v in tokens:
            if _excepted(v[0]):
                continue
            elif len(v) == 1:
                continue
            elif v[1] == "名詞":
                nouns.append(v)
            elif v[1] == "動詞":
                verbs.append(v)
            elif v[1] == "形容詞":
                adjectives.append(v)
            elif v[1] == "副詞":
                adverbs.append(v)
            elif v[1] == "接続詞":
                conjuctions.append(v)
            elif v[1] == "感動詞":
                interjections.append(v)
            elif v[1] == "助動詞":
                auxverbs.append(v)
            elif v[1] == "助詞":
                particles.append(v)
            elif v[1] == "記号":
                marks.append(v)
            elif v[1] == "接頭詞":
                prefixs.append(v)
            else:
                others.append(v)
        return {
                WordClasses.NOUN.name: nouns,
                WordClasses.VERB.name: verbs,
                WordClasses.ADJECTIVE.name: adjectives,
                WordClasses.ADVERB.name: adverbs,
                WordClasses.CONJUCTION.name: conjuctions,
                WordClasses.INTERJECTION.name: interjections,
                WordClasses.AUXVERB.name: auxverbs,
                WordClasses.PARTICLE.name: particles,
                WordClasses.MARK.name: marks,
                WordClasses.PREFIX.name: prefixs,
                WordClasses.OTHER.name: others,
                }

