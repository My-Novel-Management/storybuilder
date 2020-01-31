# -*- coding: utf-8 -*-
"""Define class that world management.
"""
## public libs
import argparse
import datetime
## local libs
from utils import assertion
from utils.util_str import dictFromStrBySplitter
from utils.utildict import UtilityDict
## local files
from builder import __BASE_COLUMN__, __BASE_ROW__
from builder import __PREFIX_DAY__
from builder import __PREFIX_STAGE__, __SUFFIX_STAGE_INT__, __SUFFIX_STAGE_EXT__
from builder import __PREFIX_TIME__, __PREFIX_WORD__
from builder import __MECAB_LINUX1__, __MECAB_LINUX2__
from builder import __PRIORITY_NORMAL__, __PRIORITY_MAX__, __PRIORITY_MIN__
from builder import __TAG_PREFIX__
from builder import __DEF_FILENAME__
from builder import __ASSET_ELEMENTS__
from builder import __DEF_YEAR__, __DEF_MON__, __DEF_DAY__
from builder import ActType, MetaType, TagType
from builder import History
from builder.action import Action
from builder.area import Area
from builder.block import Block
from builder.buildtool import Build
from builder.chapter import Chapter
from builder.converter import Converter
from builder.day import Day
from builder.episode import Episode
from builder.item import Item
from builder.layer import Layer
from builder.lifenote import LifeNote
from builder.metadata import MetaData
from builder.person import Person
from builder.rubi import Rubi
from builder.scene import Scene
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word
## common data
from common.fashions import __FASHION_LAYER__, FASHION_LAYERS
from common.stages import __STAGE_LAYER__, STAGE_LAYERS
from common.foods import __FOOD_LAYER__, FOOD_LAYERS
from common.dayandtimes import __DAYTIME_LAYER__, DAYTIME_LAYERS


## define type


## define class
class World(UtilityDict):
    """Story builder world class.
    """
    __MECAB_DIRS__ = (__MECAB_LINUX1__, __MECAB_LINUX2__)
    def __init__(self, title: str, filename: str=__DEF_FILENAME__,
            mecabdir: (str, int)=__MECAB_LINUX2__):
        self._title = assertion.isStr(title)
        self._filename = assertion.isStr(filename)
        self._basedate = datetime.date(__DEF_YEAR__, __DEF_MON__, __DEF_DAY__)
        self._basearea = Area.getDefault()
        self._areas = {}
        self._rubis = {}
        self._layers = {}
        self._stagelayers = {}
        self._daytimelayers = {}
        self._fashionlayers = {}
        self._foodlayers = {}
        self._blocks = {}
        self._tags = {}
        self._lifenotes = {}
        self._histories = {}
        self._outline = "_Story description_"
        self._mecabdir = World.__MECAB_DIRS__[mecabdir] if isinstance(mecabdir, int) else (mecabdir if isinstance(mecabdir, str) else "")
        self._columns = __BASE_COLUMN__
        self._rows = __BASE_ROW__

    ## property
    @property
    def areas(self) -> dict:
        return self._areas

    @property
    def basearea(self) -> Area:
        return self._basearea

    @property
    def basedate(self) -> datetime.date:
        return self._basedate

    @property
    def blocks(self) -> dict:
        return self._blocks

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def daytimes(self) -> dict:
        return self._daytimelayers

    @property
    def fashionlayers(self) -> dict:
        return self._fashionlayers

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def foodlayers(self) -> dict:
        return self._foodlayers

    @property
    def histories(self) -> dict:
        return self._histories

    @property
    def layers(self) -> dict:
        return self._layers

    @property
    def lifenotes(self) -> dict:
        return self._lifenotes

    @property
    def mecabdir(self) -> str:
        return self._mecabdir

    @property
    def outline(self) -> str:
        return self._outline

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def rubis(self) -> dict:
        return self._rubis

    @property
    def stagelayers(self) -> dict:
        return self._stagelayers

    @property
    def tags(self) -> dict:
        return self._tags

    @property
    def title(self) -> str:
        return self._title

    ## methods (build)
    def build(self, *args, **kwargs): # pragma: no cover
        return not self.buildStory(self.filename, self.outline, *args, **kwargs)

    def buildDB(self, persons: list, areas: list, stages: list,
            days: list, times: list,
            items: list, words: list,
            rubis: list, layers: list) -> bool: # pragma: no cover
        '''Build database
        '''
        self.setPersons(persons)
        self.setAreas(areas)
        self.setStages(stages)
        self.setDays(days)
        self.setTimes(times)
        self.setItems(items)
        self.setWords(words)
        self.setRubis(rubis)
        self.setLayers(layers)
        return True

    def buildStory(self, filename: str, outline: str, *args: Chapter,
            extention: str="", builddir: str="",
            is_testing: bool=False) -> bool: # pragma: no cover
        '''Build story object and Output creation
        '''
        opts = _optionsParsed(is_testing)
        priority = opts.pri if opts.pri else __PRIORITY_NORMAL__
        mecabdir = "" if opts.forcemecab else self.mecabdir
        formattype = opts.format
        outputpart = opts.part
        outtype = ""
        partstart, partend = 0, 0
        if outputpart and ":" in outputpart:
            tmp = outputpart.split(":")
            idx = 0
            for v in tmp:
                if idx == 0:
                    outtype = v
                elif idx == 1:
                    partstart = int(v)
                elif idx == 2:
                    partend = int(v)
                idx += 1
            if partend >= 0 and partend <= partstart:
                partend = partstart
        is_list = opts.list
        is_scenario = opts.scenario
        is_analyze = opts.analyze
        is_rubi = opts.rubi
        is_comment = opts.comment
        is_check = opts.check
        is_lifenote = opts.life
        is_conteskip = opts.skip
        is_text = opts.text
        is_debug = opts.debug
        col_row = opts.colrow
        columns, rows = self.columns, self.rows
        if col_row and ":" in col_row:
            tmp = col_row.split(":")
            columns, rows = int(tmp[0]), int(tmp[1])
        builder = Build(filename, mecabdir)
        ## compile
        src = builder.compile(self.title, priority,
                self._tags, __TAG_PREFIX__,
                self._areas,
                outtype, int(partstart) - 1, int(partend) - 1,
                outline,
                *args)
        ## sub data
        if is_list:
            builder.toBlocks(self.blocks, self._tags, __TAG_PREFIX__, is_debug)
            builder.outputLists(self, is_debug)
        if is_lifenote:
            builder.outputLifeNotes(self.lifenotes, self._tags, __TAG_PREFIX__, is_debug)
            builder.outputHistories(self.basedate, self.histories, is_debug)
        ## check
        if is_check:
            builder.checkStory(src, is_debug)
        return builder.output(src, self.rubis, self.layers,
                self.stagelayers, self.daytimes, self.fashionlayers, self.foodlayers,
                formattype,
                columns, rows,
                self.basedate, self.basearea,
                is_rubi,
                is_scenario, is_analyze,
                is_conteskip, is_text,
                is_comment, is_debug)

    def entryBlock(self, *args: Block) -> bool:
        for v in args:
            self._blocks[v.title] = assertion.isInstance(v, Block)
        return True

    def entryLifeNote(self, *args: LifeNote) -> bool:
        for v in args:
            self._lifenotes[v.title] = assertion.isInstance(v, LifeNote)
        return True

    def entryHistory(self, subject: Person, *args: History) -> bool:
        if not assertion.isInstance(subject, Person) in self._histories:
            return False
        for v in assertion.isList(args):
            self._histories[subject].append(assertion.isInstance(v, History))
        return True

    def setBaseArea(self, key: str):
        if key in self:
            self._basearea = assertion.isInstance(self[key], Area)
        return self

    def setBaseDate(self, year: int, mon: int=1, day: int=1):
        self._basedate = datetime.date(year, mon, day)
        return self

    def setColumnRow(self, col: int, row: int):
        self._columns = assertion.isInt(col)
        self._rows = assertion.isInt(row)
        return self

    def setPersons(self, persons: list):
        for v in persons:
            tmp = Person(*v[1:])
            self.__setitem__(v[0], tmp)
            last, first, full, exfull = Person.fullnamesConstructed(tmp)
            self._tags[v[0]] = tmp.name
            self._tags[f"n_{v[0]}"] = tmp.name
            self._tags[f"ln_{v[0]}"] = last
            self._tags[f"fn_{v[0]}"] = first
            self._tags[f"full_{v[0]}"] = full
            self._tags[f"exfull_{v[0]}"] = exfull
            self._histories[tmp] = []
        return self

    def setAreas(self, areas: list):
        for v in areas:
            tmp = Area(*v)
            self.__setitem__(v[0], tmp)
            self._tags[f"{v[0]}"] = tmp.name
            self._areas[tmp.tag] = tmp
        return self

    def setStages(self, stages: list):
        for v in stages:
            tmp = Stage(*v[1:])
            self.__setitem__(__PREFIX_STAGE__ + v[0], tmp)
            self._tags[f"{__PREFIX_STAGE__}{v[0]}"] = tmp.name
            tmp_int = Stage(f"{v[1]}・内", *v[2:])
            self.__setitem__(__PREFIX_STAGE__ + v[0] + __SUFFIX_STAGE_INT__, tmp_int)
            tmp_ext = Stage(f"{v[1]}・外", *v[2:])
            self.__setitem__(__PREFIX_STAGE__ + v[0] + __SUFFIX_STAGE_EXT__, tmp_ext)
        return self

    def setItems(self, items: list):
        for v in items:
            tmp = Item(*v[1:])
            self.__setitem__(v[0], tmp)
            self._tags[f"{v[0]}"] = tmp.name
        return self

    def setDays(self, days: list):
        for v in days:
            tmp = Day(*v[1:])
            self.__setitem__(__PREFIX_DAY__ + v[0], tmp)
            self._tags[f"{__PREFIX_DAY__}{v[0]}"] = tmp.name
        return self

    def setTimes(self, times: list):
        for v in times:
            tmp = Time(*v[1:])
            self.__setitem__(__PREFIX_TIME__ + v[0], tmp)
            self._tags[f"{__PREFIX_DAY__}{v[0]}"] = tmp.name
        return self

    def setWords(self, words: list):
        for v in words:
            tmp = Word(*v[1:])
            self.__setitem__(__PREFIX_WORD__ + v[0], tmp)
            self._tags[f"{__PREFIX_WORD__}{v[0]}"] = tmp.name
        return self

    def setRubis(self, rubis: list):
        for v in rubis:
            self._rubis[v[0]] = Rubi(*v)
        return self

    def setLayers(self, layers: list):
        for v in layers:
            self._layers[v[0]] = Layer(*v[1:])
        return self

    def setStageLayers(self, layers: list):
        for v in layers:
            self._stagelayers[v[0]] = Layer(*v[1:])
        return self

    def setDayTimeLayers(self, layers: list):
        for v in layers:
            self._daytimelayers[v[0]] = Layer(*v[1:])
        return self

    def setFashionLayers(self, layers: list):
        for v in layers:
            self._fashionlayers[v[0]] = Layer(*v[1:])
        return self

    def setFoodLayers(self, layers: list):
        for v in layers:
            self._foodlayers[v[0]] = Layer(*v[1:])
        return self

    def setAssets(self, assetfile: dict): # pragma: no cover
        for v in __ASSET_ELEMENTS__:
            if v.upper() in assertion.isDict(assetfile):
                if v.lower() == "persons":
                    self.setPersons(assetfile[v.upper()])
                elif v.lower() == "areas":
                    self.setAreas(assetfile[v.upper()])
                elif v.lower() == "stages":
                    self.setStages(assetfile[v.upper()])
                elif v.lower() == "days":
                    self.setDays(assetfile[v.upper()])
                elif v.lower() == "times":
                    self.setTimes(assetfile[v.upper()])
                elif v.lower() == "items":
                    self.setItems(assetfile[v.upper()])
                elif v.lower() == "words":
                    self.setWords(assetfile[v.upper()])
                elif v.lower() == "rubis":
                    self.setRubis(assetfile[v.upper()])
                elif v.lower() == "layers":
                    self.setLayers(assetfile[v.upper()])
        return self

    def setOutline(self, outline: str):
        self._outline = assertion.isStr(outline)
        return self

    def setTexture(self, key: str, texture: str):
        if key in self and isinstance(self[key], (Person, Stage, Day, Time, Item, Word)):
            self[key].setTexture(texture)
        return self

    ## methods (scenes)
    def block(self, title: str, *args, **kwargs) -> Block:
        '''Create a block
        '''
        return Block(title, *args, **kwargs)

    def chapter(self, title: str, *args, **kwargs) -> Chapter:
        '''Create a chapter
        '''
        return Chapter(title, *args, **kwargs)

    def episode(self, title: str, *args, **kwargs) -> Episode:
        '''Create a episode
        '''
        return Episode(title, *args, **kwargs)

    def history(self, date: (int, str), content: str, note: str="") -> History:
        '''Create a history
        '''
        return History(date, content, note)

    def createHistories(self, *args: (list, tuple)) -> tuple:
        def _conv(v):
            if len(assertion.isList(v)) == 2:
                return History(v[0],v[1],"")
            else:
                return History(*v)
        return tuple(_conv(v) for v in args)

    def lifenote(self, title: str, subject: Person, *args, **kwargs) -> LifeNote:
        '''Create a lifenote
        '''
        return LifeNote(title, subject, *args, **kwargs)

    def load(self, key: str) -> Block:
        '''Load entried block
        '''
        return assertion.hasKey(key, self.blocks)

    def scene(self, title: str, *args, **kwargs) -> Scene:
        '''Create a scene
        '''
        return Scene(title, *args, **kwargs)

    ## tags
    def br(self) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.BR)

    def comment(self, *args: str) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.COMMENT,
                note="。".join(args))

    def symbol(self, symbol: str) -> Action:
        return Action(act_type=ActType.TAG, tag_type=TagType.SYMBOL,
                note=symbol)

    ## meta
    def eventStart(self, title: str) -> Action:
        return self.event(title, False)

    def eventPoint(self, title: str, note: str) -> Action:
        return Action(MetaData(MetaType.EVENT_POINT, title=title, note=note), act_type=ActType.META)

    def eventEnd(self, title: str) -> Action:
        return self.event(title, True)

    def event(self, title: str, isEnd: bool=False) -> Action:
        return Action(MetaData(MetaType.EVENT_END if isEnd else MetaType.EVENT_START, title=title),
                act_type=ActType.META)

    ## utility
    def setCommonData(self): # pragma: no cover
        ''' common data setting
            0. layers
                - stage
                - day time
                - fashion
                - food
            1. area
                - zero point
        '''
        self.setStageLayers(STAGE_LAYERS)
        self.setDayTimeLayers(DAYTIME_LAYERS)
        self.setFashionLayers(FASHION_LAYERS)
        self.setFoodLayers(FOOD_LAYERS)
        def_area = Area.getDefault()
        self.setAreas([[def_area.tag, def_area.name, def_area.x, def_area.y]])
        return self

## privates
def _optionsParsed(is_testing: bool): # pragma: no cover
    '''Get and setting a commandline option.

    NOTE:
        -c, --check: using checker
        -l, --list: list output
        -s, --senario: senario mode
        -z, --analyze: analyzed info
        --colrow: set columns and rows
        --comment: output with comment
        --debug: output to console
        --forcemecab: for travis ci
        --format: set format style
        --life: lifenote and history output
        --part: part output
        --pri: set priority
        --rubi: rubi mode
        --skip: conte output skip
        --text: output description as plain text
    Returns:
        :obj:`ArgumentParser`: contain commandline options.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--check', help="using checker", action='store_true')
    parser.add_argument('-l', '--list', help="output all list", action='store_true')
    parser.add_argument('-s', '--scenario', help="output as the scenario mode", action='store_true')
    parser.add_argument('-z', '--analyze', help="output the analyzed info", action='store_true')
    parser.add_argument('--colrow', help='set columns and rows', type=str)
    parser.add_argument('--comment', help='output with comment', action='store_true')
    parser.add_argument('--debug', help="with a debug mode", action='store_true')
    parser.add_argument('--forcemecab', help='force no use mecab dir', action='store_true')
    parser.add_argument('--format', help='output the format style', type=str)
    parser.add_argument('--life', help="output person lifenotes and histories", action='store_true')
    parser.add_argument('--part', help='output the part', type=str)
    parser.add_argument('--pri', help='filter by priority(0 to 10)', type=int)
    parser.add_argument('--rubi', help='description with rubi', action='store_true')
    parser.add_argument('--skip', help='conte skipping', action='store_true')
    parser.add_argument('--text', help='output plain text', action='store_true')

    # get result
    args = parser.parse_args(args=[]) if is_testing else parser.parse_args()

    return (args)


