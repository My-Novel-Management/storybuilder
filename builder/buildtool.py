# -*- coding: utf-8 -*-
"""Define tool for build.
"""
## public libs
from collections import Counter as PyCounter
import datetime
import os
from typing import Any
## local libs
from utils import assertion
from utils.util_str import dictSorted, daytimeDictSorted
## local files
from builder import __BASE_COLUMN__, __BASE_ROW__
from builder import __FORMAT_DEFAULT__, __FORMAT_ESTAR__, __FORMAT_PHONE__, __FORMAT_WEB__
from builder import ActType, DataType
from builder import WordClasses
from builder.analyzer import Analyzer
from builder.chapter import Chapter
from builder.checker import Checker
from builder.converter import Converter
from builder.counter import Counter
from builder.day import Day
from builder.episode import Episode
from builder.extractor import Extractor
from builder.formatter import Formatter
from builder.item import Item
from builder.parser import Parser
from builder.person import Person
from builder.layer import Layer
from builder.stage import Stage
from builder.story import Story
from builder.time import Time
from builder.word import Word


class Build(object):
    """The tool class for build.
    """
    __BUILD_DIR__ = "build"
    __PERSON_DIR__ = "person"
    __ANALYZE_DIR__ = "analyze"
    __LAYER_DIR__ = "layer"
    __LIST_DIR__ = "list"
    __EXTENTION__ = "md"
    def __init__(self, filename: str, extention: str=__EXTENTION__,
            builddir: str=__BUILD_DIR__,
            column: int=__BASE_COLUMN__, row: int=__BASE_ROW__):
        self._builddir = assertion.isStr(builddir)
        self._date = datetime.date.today()
        self._extention = assertion.isStr(extention)
        self._filename = assertion.isStr(filename)
        self._column = assertion.isInt(column)
        self._row = assertion.isInt(row)

    ## property
    @property
    def builddir(self) -> str:
        return self._builddir

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def extention(self) -> str:
        return self._extention

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def column(self) -> int:
        return self._column

    @property
    def row(self) -> int:
        return self._row

    ## methods
    def compile(self, title: str, priority: int,
            tags: dict, prefix: str,
            outtype: str, start: int, end: int,
            *args) -> Story: # pragma: no cover
        ''' compile source
            1. serialize (block to actions)
            2. filter by priority
            3. replace pronouns
            4. replace tags
        '''
        tmp = Story(title, *args)
        cnv = Converter()
        tmp = cnv.srcExpandBlocks(tmp)
        tmp = cnv.srcFilterByPriority(tmp, priority)
        if outtype:
            if "c" in outtype:
                ## chapter output
                tmp = Converter.srcReducedByChapter(tmp, start, end)
            elif "e" in outtype:
                ## episode output
                tmp = Converter.srcReducedByEpisode(tmp, start, end)
        tmp = cnv.srcReplacedPronouns(tmp)
        tmp = cnv.srcReplacedTags(tmp, tags, prefix)
        return tmp

    def output(self, src: Story, rubis: dict, layers: dict,
            stages: dict, daytimes: dict, fashions: dict, foods: dict,
            mecabdir: str,
            formattype: str,
            is_rubi: bool,
            is_scenario: bool, is_analyze: bool,
            is_comment: bool, is_debug: bool) -> bool: # pragma: no cover
        '''output data
            0. basic info
            1. outline
            2. conte
            3. description (or scenario)
            4. info
                - kanji
                - wordclass
                - stage layer
                - fashion layer
                - food layer
                - time layer
                - custom layers
                - persons
        '''
        analyzer = Analyzer(mecabdir)
        ## outputs
        self.toInfoOfGeneral(src, is_debug)
        self.toOutline(src, is_debug)
        self.toConte(src, analyzer, is_debug)
        if is_scenario:
            self.toScenario(src, is_debug)
        else:
            self.toDescription(src, dictSorted(rubis), formattype, is_rubi, is_debug)
        ## informations
        self.toInfoOfKanji(src, is_debug)
        if is_analyze:
            self.toInfoOfWordClass(src, analyzer, is_debug)
        ## layers
        self.toInfoOfStages(src, dictSorted(stages), is_debug)
        self.toInfoOfFashions(src, dictSorted(fashions), is_debug)
        self.toInfoOfFoods(src, dictSorted(foods), is_debug)
        self.toInfoOfTimes(src, dictSorted(daytimes), is_debug)
        self.toInfoOfCustom(src, dictSorted(layers), is_debug)
        self.toInfoOfPersons(src, is_debug)
        ## check
        ## TODO
        #if is_analyze:
        #    self.toCheckObjects(src, is_debug)
        return True

    def outputLists(self, world: dict, is_debug: bool) -> bool:
        '''list
            - persons
            - stages
            - days
            - times
            - items
            - words
        '''
        self.toListOfPersons(world, is_debug)
        self.toListOfStages(world, is_debug)
        self.toListOfDays(world, is_debug)
        self.toListOfTimes(world, is_debug)
        self.toListOfItems(world, is_debug)
        self.toListOfWords(world, is_debug)
        return True

    def checkStory(self, src: Story, is_debug: bool) -> bool: # pragma: no cover
        # TODO
        #   - using checker
        if not Checker.validateObjects(src):
            return False
        if not Checker.validateConditions(src):
            return False
        return True

    ## methods (output data)
    def toConte(self, src: Story, analyzer: Analyzer, is_debug: bool) -> bool: # pragma: no cover
        title = f"Conte of {src.title}"
        res = Parser.toContes(src)
        return self.outputTo(Formatter.toConte(title, res, analyzer),
                self.filename, "_cnt", self.extention, self.builddir, is_debug)

    def toDescription(self, src: Story, rubis: dict, formattype: str, is_rubi: bool,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Text of {src.title}"
        ftype = __FORMAT_DEFAULT__
        ## format type
        if formattype in ("web", "w"):
            ftype = __FORMAT_WEB__
        elif formattype in ("estar", "e"):
            ftype = __FORMAT_ESTAR__
        elif formattype in ("smart", "phone", "s"):
            ftype = __FORMAT_PHONE__
        res = Parser.toDescriptionsWithRubi(src, rubis) if is_rubi else Parser.toDescriptions(src)
        return self.outputTo(Formatter.toDescription(title, res, ftype),
                self.filename, "", self.extention, self.builddir, is_debug)

    def toInfoOfCustom(self, src: Story, layers: dict,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Custom info of {src.title}"
        res = []
        for k,v in layers.items():
            res.append((DataType.HEAD, f"{k}:{v.name}"))
            res.extend(Parser.toLayerInfo(src, v.data))
        return self.outputTo(Formatter.toLayerInfo(title, res),
                self.filename, "_custom", self.extention,
                os.path.join(self.builddir, self.__LAYER_DIR__), is_debug)

    def toInfoOfFashions(self, src: Story, layers: dict,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Fashion info of {src.title}"
        res = []
        for k,v in layers.items():
            res.append((DataType.HEAD, f"{k}:{v.name}"))
            res.extend(Parser.toLayerInfo(src, v.data))
        return self.outputTo(Formatter.toLayerInfo(title, res),
                self.filename, "_fashion", self.extention,
                os.path.join(self.builddir, self.__LAYER_DIR__), is_debug)

    def toInfoOfFoods(self, src: Story, layers: dict,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Food info of {src.title}"
        res = []
        for k,v in layers.items():
            res.append((DataType.HEAD, f"{k}:{v.name}"))
            res.extend(Parser.toLayerInfo(src, v.data))
        return self.outputTo(Formatter.toLayerInfo(title, res),
                self.filename, "_food", self.extention,
                os.path.join(self.builddir, self.__LAYER_DIR__), is_debug)

    def toInfoOfGeneral(self, src: Story, is_debug: bool) -> bool: # pragma: no cover
        # TODO
        #   - colum, rowの指定を可能に。ない場合はデフォルト
        cnt = Counter()
        title = "General Info:"
        def _getTotals(v):
            return [("total", cnt.descriptions(v)),
                ("manupaper", cnt.manupaperRows(v, self.column)),
                ("rows", self.row), ("columns", self.column),
                ("chapters", cnt.chapters(v)),
                ("episodes", cnt.episodes(v)),
                ("scenes", cnt.scenes(v)),
                ("actions", cnt.actions(v))]
        def _getActtypes(v):
            tmp = [("acttype_total", cnt.actions(v))]
            for t in ActType:
                tmp.append((f"acttype {t.name}", cnt.actType(v,t)))
            return tmp
        res_base = _getTotals(src)
        res_addition = _getActtypes(src)
        def _alwaysDisplayOnConsole(infodata, is_debug):
            if not is_debug:
                self.outputToConsole(infodata)
            return infodata
        _alwaysDisplayOnConsole(Formatter.toGeneralInfo(title,
            [(DataType.DATA_DICT, dict(res_base))], False), is_debug)
        ## outputs
        res = Formatter.toGeneralInfo(title,
                    [(DataType.DATA_DICT, dict(res_base + res_addition))])
        scenes = Extractor.scenesFrom(src)
        tmp = []
        for sc in scenes:
            tmp.append((DataType.HEAD, sc.title))
            tmp.append((DataType.DATA_DICT,
                dict(_getTotals(sc) + _getActtypes(sc))))
        res_scenes = Formatter.toGeneralInfoEachScene("Each Scenes:", tmp)
        return self.outputTo(res + res_scenes,
                self.filename, "_info", self.extention, self.builddir, is_debug)

    def toInfoOfKanji(self, src: Story, is_debug: bool): # pragma: no cover
        title = f"Kanji info of {src.title}"
        total = Counter.descriptions(src)
        kanji = Counter.kanjis(src)
        res = [(DataType.DATA_DICT,
                {"total": total,
                    "kanji": kanji})]
        for sc in Extractor.scenesFrom(src):
            res.append((DataType.HEAD, sc.title))
            res.append((DataType.DATA_DICT,
                {"total": Counter.descriptions(sc),
                    "kanji": Counter.kanjis(sc),
                    }))
        return self.outputTo(Formatter.toKanjiInfo(title, res),
                self.filename, "_kanji", self.extention,
                os.path.join(self.builddir, self.__ANALYZE_DIR__), is_debug)

    def toInfoOfPersons(self, src: Story, is_debug: bool) -> bool: # pragma: no cover
        # TODO
        #   - dialogue
        persons = Extractor.personAndSubjectsFrom(src)
        def _buildLayer(p: Person):
            last, first, full, exfull = Person.fullnamesConstructed(p)
            tmp = Layer(p.name,
                    (p.name, last, first, full, exfull))
            return tmp
        is_succeeded = True
        for p in persons:
            lay = _buildLayer(p)
            title = f"Persons info of {p.name}"
            res = Parser.toLayerInfo(src, lay.data)
            is_succeeded = self.outputTo(Formatter.toLayerInfo(title, res),
                p.name, "", self.extention,
                os.path.join(self.builddir, self.__PERSON_DIR__), is_debug)
            if not is_succeeded:
                AssertionError("Person info error!", p)
        return is_succeeded

    def toInfoOfStages(self, src: Story, layers: dict,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Stage info of {src.title}"
        res = []
        for k,v in layers.items():
            res.append((DataType.HEAD, f"{k}:{v.name}"))
            res.extend(Parser.toLayerInfo(src, v.data))
        return self.outputTo(Formatter.toLayerInfo(title, res),
                self.filename, "_stage", self.extention,
                os.path.join(self.builddir, self.__LAYER_DIR__), is_debug)

    def toInfoOfTimes(self, src: Story, layers: dict,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Day Time info of {src.title}"
        res = []
        for k,v in layers.items():
            res.append((DataType.HEAD, f"{k}:{v.name}"))
            res.extend(Parser.toLayerInfo(src, v.data))
        return self.outputTo(Formatter.toLayerInfo(title, res),
                self.filename, "_daytime", self.extention,
                os.path.join(self.builddir, self.__LAYER_DIR__), is_debug)

    def toInfoOfWordClass(self, src: Story, analyzer: Analyzer,
            is_debug: bool) -> bool: # pragma: no cover
        title = f"Word class info of {src.title}"
        wcls = analyzer.collectionsWordClassByMecab(src)
        res = []
        def _create(title, name):
            base = PyCounter([v[0] for v in wcls[name]])
            maxnum = base.most_common()[0][1] if base.most_common() else 0
            res.append((DataType.HEAD, title))
            for i in reversed(range(maxnum)):
                tmp = []
                for w,c in base.most_common():
                    if c == i + 1:
                        tmp.append(w)
                if tmp:
                    res.append((DataType.DATA_STR, f"{i + 1}: {','.join(tmp)}"))
        for v in WordClasses:
            _create(v.value, v.name)
        return self.outputTo(Formatter.toWordClassInfo(title, res),
                self.filename, "_wordcls", self.extention,
                os.path.join(self.builddir, self.__ANALYZE_DIR__), is_debug)

    def toOutline(self, src: Story, is_debug: bool) -> bool: # pragma: no cover
        title = f"Outline of {src.title}"
        res = Parser.toOutlines(src)
        return self.outputTo(Formatter.toOutline(title, res),
                self.filename, "_out", self.extention, self.builddir, is_debug)

    def toScenario(self, src: Story, is_debug: bool) -> bool: # pragma: no cover
        # TODO
        print("__unimplement scenario mode__")
        return True

    ## to list
    def toListOfDays(self, src: dict, is_debug: bool) -> bool:
        days = daytimeDictSorted(self.getFromWorld(src, Day), False)
        title = f"Days list of {src.title}"
        res = [(DataType.DATA_DICT,dict([(k,v) for k,v in days.items()]))]
        return self.outputTo(Formatter.toListDayTimes(title, res),
                self.filename, "_days", self.extention,
                os.path.join(self.builddir, self.__LIST_DIR__), is_debug)

    def toListOfItems(self, src: dict, is_debug: bool) -> bool:
        items = dictSorted(self.getFromWorld(src, Item), False)
        title = f"Items list of {src.title}"
        res = [(DataType.DATA_DICT, dict([(k,v) for k,v in items.items()]))]
        return self.outputTo(Formatter.toListInfo(title, res),
                self.filename, "_items", self.extention,
                os.path.join(self.builddir, self.__LIST_DIR__), is_debug)

    def toListOfPersons(self, src: dict, is_debug: bool) -> bool:
        persons = dictSorted(self.getFromWorld(src, Person), False)
        title = f"Persons list of {src.title}"
        res = [(DataType.DATA_DICT, dict([(k, v) for k,v in persons.items()]))]
        return self.outputTo(Formatter.toListPersons(title, res),
                self.filename, "_persons", self.extention,
                os.path.join(self.builddir, self.__LIST_DIR__), is_debug)

    def toListOfStages(self, src: dict, is_debug: bool) -> bool:
        stages = dictSorted(dict([(k,v) for k,v in self.getFromWorld(src, Stage).items() if not ("_int" in k or "_ext" in k)]), False)
        title = f"Stages list of {src.title}"
        res = [(DataType.DATA_DICT, dict([(k,v) for k,v in stages.items()]))]
        return self.outputTo(Formatter.toListInfo(title, res),
                self.filename, "_stages", self.extention,
                os.path.join(self.builddir, self.__LIST_DIR__), is_debug)

    def toListOfTimes(self, src: dict, is_debug: bool) -> bool:
        times = daytimeDictSorted(self.getFromWorld(src, Time), False)
        title = f"Times list of {src.title}"
        res = [(DataType.DATA_DICT, dict([(k,v) for k,v in times.items()]))]
        return self.outputTo(Formatter.toListDayTimes(title, res),
                self.filename, "_times", self.extention,
                os.path.join(self.builddir, self.__LIST_DIR__), is_debug)

    def toListOfWords(self, src: dict, is_debug: bool) -> bool:
        words = dictSorted(self.getFromWorld(src, Word), False)
        title = f"Words list of {src.title}"
        res = [(DataType.DATA_DICT, dict([(k,v) for k,v in words.items()]))]
        return self.outputTo(Formatter.toListInfo(title, res),
                self.filename, "_words", self.extention,
                os.path.join(self.builddir, self.__LIST_DIR__), is_debug)

    ## methods (output)
    def outputTo(self, data: list, filename: str, suffix: str, extention: str,
            builddir: str, is_debug: bool) -> bool: # pragma: no cover
        if is_debug:
            return self.outputToConsole(data)
        else:
            return self.outputToFile(data, filename, suffix, extention, builddir)

    def outputToConsole(self, data: list) -> bool: # pragma: no cover
        for v in data:
            print(v)
        return True

    def outputToFile(self, data: list, filename: str, suffix: str, extention: str,
            builddir: str) -> bool: # pragma: no cover
        if not os.path.isdir(builddir):
            os.makedirs(builddir)
        fullpath = os.path.join(builddir, "{}{}.{}".format(
            assertion.isStr(filename), assertion.isStr(suffix),
            assertion.isStr(extention)
            ))
        with open(fullpath, 'w') as f:
            for v in data:
                f.write(f"{v}\n")
        return True

    ## method (for world utility)
    @classmethod
    def getFromWorld(cls, src: dict, obj: Any) -> dict:
        return dict([(k,v) for k,v in src.items() if isinstance(v, obj)])
