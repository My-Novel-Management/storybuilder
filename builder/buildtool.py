# -*- coding: utf-8 -*-
"""The build tool.
"""
from __future__ import print_function
from itertools import chain
import os
import argparse
import re
from . import assertion
from .world import World
from .story import Story
from .parser import Parser
from .strutils import dict_sorted
from .analyzer import Analyzer
from .converter import Converter
from .extractor import Extractor
from .formatter import Formatter
from .chara import Chara
from .person import Person
from . import __DEF_PRIORITY__


class Build(object):
    """The story build tools.
    """
    __FILENAME__ = "story"
    __EXTENSION__ = "md" # NOTE: currently markdown only
    __BUILD_DIR__ = "build"

    def __init__(self, story: Story, world_dict: dict, rubi_dict: dict,
            opt_dic: str="",
            is_debug_test: bool=False):
        self._story = Build._validatedStory(story)
        self._rubis = dict_sorted(assertion.is_dict(rubi_dict))
        self._words = assertion.is_dict(world_dict)
        self._filename = Build.__FILENAME__
        self._options = _options_parsed(is_debug_test)
        self._extension = Build.__EXTENSION__
        self._builddir = Build.__BUILD_DIR__
        self._mecabdictdir = assertion.is_str(opt_dic)
        # TODO: build dir を指定（変更）できるように

    @staticmethod
    def constractWords(world: World): # pragma: no cover
        return Build._wordsFrom(world)

    # methods
    def output_story(self): # pragma: no cover
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
            is_succeeded = self.to_outline(parser, filename, is_debug)
            if not is_succeeded:
                print("ERROR: output a outline failed!!")
                return is_succeeded

        if options.scenario:
            is_succeeded = self.to_scenario(parser, filename, is_comment, is_debug)
            if not is_succeeded:
                print("ERROR: output a scenario failed!!")
                return is_succeeded

        if options.description:
            is_succeeded = self.to_description(parser, filename, formattype,
                    self._rubis,
                    is_comment, options.rubi, is_debug)
            if not is_succeeded:
                print("ERROR: output a description failed!!")
                return is_succeeded

        if options.action:
            # TODO: action view output
            pass

        if options.info:
            # TODO: detail info output
            is_succeeded = self.to_detail_info(parser, analyzer, filename,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a detail info failed!!")
                return is_succeeded

        if options.analyze:
            # TODO: analyze documents
            is_succeeded = self.to_analyzed_info(parser, analyzer, filename,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output an analyzed info failed!!")
                return is_succeeded

        if options.layer:
            is_succeeded = self.to_layer(parser, filename, is_debug)
            if not is_succeeded:
                print("ERROR: output a description failed!!")
                return is_succeeded

        if options.person:
            # TODO: show character infos
            pass

        if options.dialogue:
            is_succeeded = self.to_dialogue_info(parser, analyzer, filename,
                    is_debug)
            if not is_succeeded:
                print("ERROR: output a dialogue info failed!!")
                return is_succeeded

        if options.version:
            # TODO: show version
            pass

        # total info (always display)
        is_succeeded = self.to_total_info(parser, analyzer)

        return is_succeeded

    def to_analyzed_info(self, parser: Parser, analyzer: Analyzer, filename: str,
            is_debug: bool): # pragma: no cover
        # NOTE: 解析結果
        freq = analyzer.frequency_words(parser.src)
        res = freq
        return self.outputOn(res, filename, "_anal", self._extension, self._builddir, is_debug)

    def to_description(self, parser: Parser, filename: str, formattype: str,
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

    def to_detail_info(self, parser: Parser, analyzer: Analyzer, filename: str,
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
        return self.outputOn(res, filename, "_info", self._extension, self._builddir, is_debug)

    def to_dialogue_info(self, parser: Parser, analyzer: Analyzer, filename: str,
            is_debug: bool): # pragma: no cover
        # NOTE: dialogue count and list
        info = Formatter().toDialoguesInfo(
                analyzer.dialoguesEachPerson(parser.src))
        res = ["# Dialogues info\n"] \
                + info
        return self.outputOn(res, filename, "_dial", self._extension, self._builddir, is_debug)

    def to_layer(self, parser:Parser, filename: str, is_debug: bool): # pragma: no cover
        res = Formatter().toDescriptionsAsLayer(parser.toDescriptionsAsLayer())
        res_outline = Formatter().toOutlinesAsLayer(parser.toOutlinesAsLayer())
        if is_debug:
            res_outline = ["---- outline ----"] + res_outline
        return self.outputOn(res, filename, "_lay", self._extension, self._builddir, is_debug) \
                and self.outputOn(res_outline, filename, "_layO", self._extension, self._builddir, is_debug)

    def to_outline(self, parser: Parser, filename: str, is_debug: bool): # pragma: no cover
        res = Formatter().toOutlines(parser.toOutlines())
        return self.outputOn(res, filename, "_out", self._extension, self._builddir, is_debug)

    def to_scenario(self, parser: Parser, filename: str, is_comment: bool,
            is_debug: bool): # pragma: no cover
        res = Formatter().toScenarios(parser.toScenarios())
        return self.outputOn(res, filename, "_sc", self._extension, self._builddir, is_debug)

    def to_total_info(self, parser: Parser, analyzer: Analyzer): # pragma: no cover
        charcounts = Formatter().toCharactersInfo(
                analyzer.charactersCount(parser.src))
        return Build._out_to_console(charcounts)

    def outputOn(self, data: list, filename: str, suffix: str, extention: str,
            builddir: str, is_debug: bool): # pragma: no cover
        if is_debug:
            return Build._out_to_console(data)
        else:
            return Build._out_to_file(data, filename, suffix, extention, builddir)

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
            if isinstance(v, Chara):
                tmp_persons.append((k, v.name))
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

    def _out_to_console(data: list): # pragma: no cover
        is_succeeded = True
        for v in data:
            print(v)
        return is_succeeded

    def _out_to_file(data: list, filename: str, suffix: str, extention: str,
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
def _options_parsed(is_debug_test: bool): # pragma: no cover
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
    parser.add_argument('-i', '--info', help="output adding the detail info", action='store_true')
    parser.add_argument('-z', '--analyze', help="output the analyzed info", action='store_true')
    parser.add_argument('-l', '--layer', help="output using the layer", action='store_true')
    # TODO: character info
    parser.add_argument('-p', '--person', help="output characters info", action='store_true')
    parser.add_argument('-c', '--dialogue', help="output character dialogues and conversations", action='store_true')
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


