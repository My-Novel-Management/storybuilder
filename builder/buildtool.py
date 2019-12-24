# -*- coding: utf-8 -*-
"""The build tool.
"""
from __future__ import print_function
from itertools import chain
import os
import argparse
import re
from . import __DEF_PRIORITY__
from . import STAGE_LAYERS
from . import FASHION_LAYERS
from . import FOOD_LAYERS
from . import assertion
from .action import Layer
from .basesubject import NoSubject
from .world import World
from .story import Story
from .parser import Parser
from .strutils import dict_sorted
from .analyzer import Analyzer
from .converter import Converter
from .extractor import Extractor
from .formatter import Formatter
from .person import Person


class Build(object):
    """The story build tools.
    """
    __FILENAME__ = "story"
    __EXTENSION__ = "md" # NOTE: currently markdown only
    __BUILD_DIR__ = "build"

    def __init__(self, story: Story, world_dict: dict,
            rubi_dict: dict,
            layer_dict: dict,
            opt_dic: str="",
            is_debug_test: bool=False):
        self._story = Build._validatedStory(story)
        self._rubis = dict_sorted(assertion.is_dict(rubi_dict))
        self._layers = dict_sorted(assertion.is_dict(layer_dict))
        self._words = assertion.is_dict(world_dict)
        self._filename = Build.__FILENAME__
        self._options = _optionsParsed(is_debug_test)
        self._extension = Build.__EXTENSION__
        self._builddir = Build.__BUILD_DIR__
        self._mecabdictdir = assertion.is_str(opt_dic)
        # TODO: build dir を指定（変更）できるように

    @staticmethod
    def constractWords(world: World): # pragma: no cover
        return Build._wordsFrom(world)

    # methods
    def outputStory(self): # pragma: no cover
        is_succeeded = True
        options = self._options
        filename = self._filename # TODO: ファイル名指定できるようにする
        pri_filter = options.pri # TODO: priority指定できるようにする
        formattype = options.format
        is_debug = options.debug # NOTE: 現在デバッグモードはコンソール出力のみ
        is_comment = options.comment # NOTE: コメント付き出力

        story_converted = Converter(self._story).toConvertFullSrc(pri_filter, self._words)
        parser = Parser(story_converted)
        _mecabdir = self._mecabdictdir
        if options.forcemecab:
            _mecabdir = ""
        elif options.mecab:
            _mecabdir = options.mecab
        analyzer = Analyzer(_mecabdir)

        if options.outline:
            is_succeeded = self.toOutline(parser, filename, is_debug)
            if not is_succeeded:
                print("ERROR: output a outline failed!!")
                return is_succeeded

        if options.scenario:
            is_succeeded = self.toScenario(parser, filename, is_comment, is_debug)
            if not is_succeeded:
                print("ERROR: output a scenario failed!!")
                return is_succeeded

        if options.description:
            is_succeeded = self.toDescription(parser, filename, formattype,
                    self._rubis,
                    is_comment, options.rubi, is_debug)
            if not is_succeeded:
                print("ERROR: output a description failed!!")
                return is_succeeded

        if options.action:
            # TODO: action view output
            pass

        if options.info:
            # NOTE:
            #   0. char count
            is_succeeded = self.toDetailInfo(parser, analyzer, filename,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a detail info failed!!")
                return is_succeeded

        if options.detail:
            # NOTE:
            #   1. words layers
            #   2. stage layers
            #   3. fashion layers
            #   4. food layers
            is_succeeded = self.toDetailByWords(parser, analyzer, filename,
                    self._layers,
                    "Words", 1,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a detail info1(words) failed!!")
                return is_succeeded

            is_succeeded = self.toDetailByWords(parser, analyzer, filename,
                    _layerDictFrom(STAGE_LAYERS),
                    "Stages", 2,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a detail info2(stages) failed!!")
                return is_succeeded

            is_succeeded = self.toDetailByWords(parser, analyzer, filename,
                    _layerDictFrom(FASHION_LAYERS),
                    "Fashions", 3,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a detail info3(fashions) failed!!")
                return is_succeeded

            is_succeeded = self.toDetailByWords(parser, analyzer, filename,
                    _layerDictFrom(FOOD_LAYERS),
                    "Foods", 4,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a detail info4(foods) failed!!")
                return is_succeeded

        if options.person:
            is_succeeded = self.toPersonInfo(parser, analyzer, filename, is_debug)

        if options.analyze:
            # TODO: analyze documents
            is_succeeded = self.toAnalyzedInfo(parser, analyzer, filename,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output an analyzed info failed!!")
                return is_succeeded

        if options.layer:
            is_succeeded = self.toLayer(parser, filename, is_debug)
            if not is_succeeded:
                print("ERROR: output a description failed!!")
                return is_succeeded

        if options.person:
            # TODO: show character infos
            pass

        if options.dialogue:
            is_succeeded = self.toDialogueInfo(parser, analyzer, filename,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a dialogue info failed!!")
                return is_succeeded

        if options.version:
            # TODO: show version
            pass

        # total info (always display)
        is_succeeded = self.toTotalInfo(parser, analyzer)

        return is_succeeded

    def toAnalyzedInfo(self, parser: Parser, analyzer: Analyzer, filename: str,
            is_debug: bool): # pragma: no cover
        # NOTE: 解析結果
        freq = analyzer.frequency_words(parser.src)
        res = freq
        return self.outputOn(res, filename, "_anal", self._extension, self._builddir, is_debug)

    def toDescription(self, parser: Parser, filename: str, formattype: str,
            rubi_dict: dict,
            is_comment: bool, rubi: bool, is_debug: bool): # pragma: no cover
        res = Formatter().toDescriptions(parser.toDescriptions(is_comment))
        if rubi:
            res = Formatter().toDescriptions(
                    parser.toDescriptionsWithRubi(rubi_dict, is_comment))
        if formattype in ("estar",):
            res = Formatter().toDescriptionsAsEstar(res)
        elif formattype in ("smart", "phone"):
            res = Formatter().toDescriptionsAsSmartphone(res)
        elif formattype in ("web",):
            res = Formatter().toDescriptionsAsWeb(res)
        return self.outputOn(res, filename, "", self._extension, self._builddir, is_debug)

    def toDetailInfo(self, parser: Parser, analyzer: Analyzer, filename: str,
            is_debug: bool): # pragma: no cover
        # TODO: 最初にタイトルから章やシーンリスト
        # TODO: 文字数に続いて各シーンの簡易情報
        # TODO: 各分析情報
        # TODO: flag情報
        # TODO: Formatterを使うようにする
        extr = Extractor(parser.src)
        total_charcounts = Formatter().toCharactersInfo(
                analyzer.charactersCount(parser.src), "Total", 0)
        scenes_charcounts = Formatter().toCharactersInfoEachScenes(
                analyzer.charactersCountEachScenes(parser.src)
                )
        acts_percent = Formatter().toActionPercentInfo(
                analyzer.actionsCount(parser.src),
                analyzer.actionsPercent(parser.src), "")
        scenes_actspercent = Formatter().toActionPercentInfoEachScenes(
                analyzer.actionsTotalsFrom(parser.src),
                analyzer.actionsPercentEachScenes(parser.src)
                )
        flaginfo = ["## Flags info\n"] + Formatter().toFlagsInfo(
                analyzer.flagsFrom(parser.src)
                )
        head = [f"# Detail information of {parser.src.title}\n"]
        res = head \
                + ["## Characters info\n"] \
                + total_charcounts \
                + scenes_charcounts \
                + ["\n## Actions info\n"] \
                + acts_percent + [""] \
                + scenes_actspercent + [""] \
                + flaginfo
        return self.outputOn(res, filename, "_info0", self._extension, self._builddir, is_debug)

    def toDetailByWords(self, parser: Parser, analyzer: Analyzer, filename: str,
            layers: dict,
            title: str,
            num: int,
            is_debug: bool) -> bool: # pragma: no cover
        tmp = []
        for k,v in layers.items():
            tmp.append([("Title", f"\n## About {k}:{v.name}\n")])
            tmp.append(analyzer.descsHasWords(parser.src, v.words))
        res = [f"# Analyzed {title} info of {parser.src.title}\n"] \
                + Formatter().toLayersInfo(list(chain.from_iterable(tmp)))
        return self.outputOn(res, filename, f"_info{num}", self._extension, self._builddir,
                is_debug)

    def toDialogueInfo(self, parser: Parser, analyzer: Analyzer, filename: str,
            is_debug: bool): # pragma: no cover
        # NOTE: dialogue count and list
        info = Formatter().toDialoguesInfo(
                analyzer.dialoguesEachPerson(parser.src))
        res = ["# Dialogues info\n"] \
                + info
        return self.outputOn(res, filename, "_dial", self._extension, self._builddir, is_debug)

    def toLayer(self, parser:Parser, filename: str, is_debug: bool): # pragma: no cover
        res = Formatter().toDescriptionsAsLayer(parser.toDescriptionsAsLayer())
        res_outline = Formatter().toOutlinesAsLayer(parser.toOutlinesAsLayer())
        if is_debug:
            res_outline = ["---- outline ----"] + res_outline
        return self.outputOn(res, filename, "_lay", self._extension, self._builddir, is_debug) \
                and self.outputOn(res_outline, filename, "_layO", self._extension, self._builddir, is_debug)

    def toOutline(self, parser: Parser, filename: str, is_debug: bool): # pragma: no cover
        res = Formatter().toOutlines(parser.toOutlines())
        return self.outputOn(res, filename, "_out", self._extension, self._builddir, is_debug)

    def toPersonInfo(self, parser: Parser, analyzer: Analyzer, filename: str, is_debug: bool) -> bool: # pragma: no cover
        is_succeeded = False
        builddir = self._builddir + "/person"
        persons = Extractor(parser.src).persons
        def _buildLayer(p: Person):
            tmp = Layer(p.name,
                    (p.name, p.fullname, p.lastname, p.firstname))
            return tmp
        for v in persons:
            if isinstance(v, NoSubject):
                continue
            lay = _buildLayer(v)
            tmp = []
            tmp.append([("Title", f"\n## About {v.name}\n")])
            tmp.append([("Head", f"* Contains words")])
            tmp.append(analyzer.descsHasWords(parser.src, lay.words))
            tmp.append([("Head", f"\n* Subject actions")])
            tmp.append(analyzer.descriptionsOfPerson(parser.src, v))
            tmp.append([("Head", f"\n* Dialogues")])
            tmp.append(analyzer.dialoguesOfPerson(parser.src, v))
            res = Formatter().toLayersInfo(list(chain.from_iterable(tmp)))
            is_succeeded = self.outputOn(res, v.name, "", self._extension, builddir, is_debug)
            if not is_succeeded:
                raise AssertionError(f"person (v.name) info output error: ", v)
        return is_succeeded

    def toScenario(self, parser: Parser, filename: str, is_comment: bool,
            is_debug: bool): # pragma: no cover
        res = Formatter().toScenarios(parser.toScenarios())
        return self.outputOn(res, filename, "_sc", self._extension, self._builddir, is_debug)

    def toTotalInfo(self, parser: Parser, analyzer: Analyzer): # pragma: no cover
        charcounts = Formatter().toCharactersInfo(
                analyzer.charactersCount(parser.src))
        return Build._outToConsole(charcounts)

    def outputOn(self, data: list, filename: str, suffix: str, extention: str,
            builddir: str, is_debug: bool): # pragma: no cover
        if is_debug:
            return Build._outToConsole(data)
        else:
            return Build._outToFile(data, filename, suffix, extention, builddir)

    # private
    def _validatedStory(story: Story):
        if isinstance(story, Story):
            return story
        else:
            raise AssertionError("Must be data type of 'Story'!")
        return False

    def _wordsFrom(world: World):
        '''To create the world dictionary.
        '''
        tmp = {}
        # persons and charas
        tmp_persons = []
        for k, v in assertion.is_instance(world, World).items():
            if k in ('stage', 'day', 'time', 'item', 'word'):
                continue
            elif isinstance(v, Person):
                tmp_persons.append((f"n_{k}", v.name))
                tmp_persons.append((f"fn_{k}", v.firstname))
                tmp_persons.append((f"ln_{k}", v.lastname))
                tmp_persons.append((f"full_{k}", v.fullname))
                tmp_persons.append((f"efull_{k}", v.exfullname))
        tmp_stages = [(f"st_{k}", v.name) for k,v in world.stage.items()]
        tmp_items = [(f"t_{k}", v.name) for k,v in world.item.items()]
        tmp_words = [(f"w_{k}", v.name) for k,v in world.word.items()]
        return dict_sorted(dict(tmp_persons + tmp_stages + tmp_items + tmp_words))

    def _outToConsole(data: list): # pragma: no cover
        is_succeeded = True
        for v in data:
            print(v)
        return is_succeeded

    def _outToFile(data: list, filename: str, suffix: str, extention: str,
            builddir: str): # pragma: no cover
        is_succeeded = True
        if not os.path.isdir(builddir):
            os.makedirs(builddir)
        fullpath = os.path.join(builddir, "{}{}.{}".format(
            assertion.is_str(filename), assertion.is_str(suffix),
            assertion.is_str(extention)
            ))
        with open(fullpath, 'w') as f:
            for v in data:
                f.write(f"{v}\n")
        return is_succeeded

# privates
def _layerDictFrom(data: list) -> dict:
    tmp = {}
    for v in assertion.is_list(data):
        k, val = v[0], v[1:]
        tmp[k] = Layer(*val)
    return tmp

def _optionsParsed(is_debug_test: bool): # pragma: no cover
    '''Get and setting a commandline option.

    Returns:
        :obj:`ArgumentParser`: contain commandline options.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outline', help="output the outline", action='store_true')
    parser.add_argument('-s', '--scenario', help="output the scenario", action='store_true')
    parser.add_argument('-d', '--description', help="output the novel", action='store_true')
    # TODO: action view
    parser.add_argument('-a', '--action', help="output the monitoring action", action='store_true')
    parser.add_argument('-i', '--info', help="output the abstract info", action='store_true')
    parser.add_argument('--detail', help="output the detail informations", action='store_true')
    parser.add_argument('-z', '--analyze', help="output the analyzed info", action='store_true')
    parser.add_argument('-l', '--layer', help="output using the layer", action='store_true')
    # TODO: character info
    parser.add_argument('-p', '--person', help="output characters info", action='store_true')
    parser.add_argument('--dialogue', help="output character dialogues and conversations", action='store_true')
    # TODO: help
    # TODO: version info
    parser.add_argument('-v', '--version', help="display this version", action='store_true')
    # TODO: advanced file name
    parser.add_argument('-f', '--file', help="advanced output the file name", type=str)
    # TODO: priority setting
    parser.add_argument('--pri', help="output filtered by the priority", type=int, default=__DEF_PRIORITY__)
    parser.add_argument('--debug', help="with a debug mode", action='store_true')
    parser.add_argument('--format', help='output the format style', type=str)
    parser.add_argument('--comment', help='output with comment', action='store_true')
    parser.add_argument('--mecab', help='force using the mecab dictionary directory', type=str)
    parser.add_argument('--forcemecab', help='force no use mecab dir', action='store_true')
    parser.add_argument('--rubi', help='description with rubi', action='store_true')

    # get result
    args = parser.parse_args(args=[]) if is_debug_test else parser.parse_args()

    return (args)


