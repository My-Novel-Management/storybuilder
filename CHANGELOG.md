# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.1-4] - 2020-02-26
### Fixed
- rubi: kotatsu

## [0.5.1-3] - 2020-02-18
### Fixed
- rubi

## [0.5.1-2] - 2020-02-18
### Fixed
- format invalid breakline

## [0.5.1-1] - 2020-02-01
### Added
- episode char count in description

## [0.5.1] - 2020-02-01
### Added
- description output with scene char count

## [0.5.0] - 2020-02-01
### Added
- continued action

## [0.4.5-7] - 2020-01-31
### Changed
- person line format

## [0.4.5-6] - 2020-01-31
### Added
- person line output
### Changed
- stage and event line output dir

## [0.4.5-5] - 2020-01-31
### Fixed
- event point string longer

## [0.4.5-4] - 2020-01-31
### Fixed
- event line scene title

## [0.4.5-3] - 2020-01-31
### Changed
- event line format
### Fixed
- stage and area cooperation

## [0.4.5-2] - 2020-01-30
### Fixed
- Asset file names

## [0.4.5-1] - 2020-01-30
### Fixed
- Area not set bug

## [0.4.5] - 2020-01-30
### Added
- Area data class

## [0.4.4-5] - 2020-01-29
### Added
- elapsed day

## [0.4.4-4] - 2020-01-29
### Added
- Asset: acccessory
### Changed
- block output using list switch
### Fixed
- time delta in Stageline

## [0.4.4-3] - 2020-01-28
### Fixed
- duplicated maru in Conte

## [0.4.4-2] - 2020-01-28
### Added
- Time object new attr and methods: elapsed time

## [0.4.4-1] - 2020-01-28
### Fixed
- desc char count: except wear action strings

## [0.4.4] - 2020-01-28
### Changed
- object texture: single data from dict

## [0.4.3-33] - 2020-01-28
### Added
- scene objects output on Conte

## [0.4.3-32] - 2020-01-28
### Changed
- block info output using tags
### Fixed
- action object dupulicated when dividing actions

## [0.4.3-31] - 2020-01-28
### Changed
- stage line format

## [0.4.3-30] - 2020-01-27
### Fixed
- question and kakko bug: invalid inserting a space

## [0.4.3-29] - 2020-01-27
### Changed
- look action and subject display format on conte

## [0.4.3-28] - 2020-01-27
### Fixed
- combine to description bug: divided action

## [0.4.3-27] - 2020-01-27
### Changed
- stage line output format: time delta arrow

## [0.4.3-26] - 2020-01-27
### Added
- info volume output

## [0.4.3-25] - 2020-01-26
### Added
- event line output
### Changed
- stage line format

## [0.4.3-24] - 2020-01-26
### Added
- meta data: event

## [0.4.3-23] - 2020-01-26
### Fixed
- info tag convert

## [0.4.3-22] - 2020-01-25
### Added
- block title display on conte

## [0.4.3-21] - 2020-01-25
### Fixed
- part output end number

## [0.4.3-20] - 2020-01-24
### Fixed
- part output number

## [0.4.3-19] - 2020-01-24
### Added
- action per person output

## [0.4.3-18] - 2020-01-23
### Fixed
- conte output in action do with item object

## [0.4.3-17] - 2020-01-23
### Fixed
- kigou with spacing bug: invalid inserted

## [0.4.3-16] - 2020-01-21
### Fixed
- who bug: invalid replacement

## [0.4.3-15] - 2020-01-21
### Added
- auto action divide

## [0.4.3-14] - 2020-01-21
### Fixed
- mecab verbs analyzer

## [0.4.3-13] - 2020-01-21
### Fixed
- writer subject using not person

## [0.4.3-12] - 2020-01-21
### Changed
- conte output format (icon adding)

## [0.4.3-11] - 2020-01-20
### Added
- chapter and episode char count output
- block info output
- stage line output
### Changed
- scene setting shared over episodes
### Fixed
- comment output always

## [0.4.3-10] - 2020-01-15
### Added
- note tag convert
- charactor count output each scene on conte

## [0.4.3-9] - 2020-01-13
### Added
- text output

## [0.4.3-8] - 2020-01-13
### Fixed
- tag format: br and symbol output

## [0.4.3-7] - 2020-01-12
### Added
- columns and rows setting

## [0.4.3-6] - 2020-01-12
### Fixed
- combine documents using then

## [0.4.3-5] - 2020-01-12
### Added
- set outline in world
### Fixed
- output outline maintile

## [0.4.3-4] - 2020-01-12
### Added
- note and titles counter
### Changed
- outline output format (each heads)

## [0.4.3-3] - 2020-01-10
### Fixed
- buildDB order typo

## [0.4.3-2] - 2020-01-10
### Fixed
- chapter count ouput: typo

## [0.4.3-1] - 2020-01-10
### Fixed
- output without maru using ActType.Voice

## [0.4.3] - 2020-01-08
### Added
- LifeNote
- History

## [0.4.2] - 2020-01-07
### Added
- MetaData
- Rubi
- Layer
- Pronoun
- Checker
### Removed
- Flag

## NOTE
- version 0.4.0 and 0.4.1 is fallback

## [0.3.2] - 2019-12-16
### Added
- Writer
- Scene: using when, where and who
### Changed
- Analyzer: using story containers
### Fixed
- old parser methods

## [0.3.1] - 2019-12-02
### Added
- Extractor
- Formatter
- Covnerter
- common times data
- episode char count
- Person: simple person creator
- test utility
### Changed
- Parser
- display names of values in subtest
- Analyzer: containsWord using all story containers/And or Or check enable
### Fixed
- analyzer bug
- default layer

## [0.3.0] - 2019-11-17
### Added
- action layer
- using MeCab for analyzer
- priority filter
- collect word class
- parser class
- formatter class
- test utility
- build test on travis ci
### Changed
- scene set at first time
### Fixed
- scene and episode title
- scenario symbole without maru


## [0.2.10] - 2019-11-13
### Note
- moved new repository

## [0.2.9] - 2019-10-18
### TODO
- each unit tests
### Changed
- Refining total sources
### Removed
- Old builder

## [0.2.1] - 2019-07-07
### Added
- themes and motifs checking utility
- manupapers count
- keywords checking in descriptions
- first and last name each persons (using as tag)
- person's new attributes
- emphasis description
- directly writing a description to an action
- output each scene information
### Fixed
- duplicated output with info option
- empty main title error
- nodesc class checkout

## [0.2.0] - 2019-04-27
### Added
- Analyzer methods from tools
- Parser methods from tools
### Changed
- assertion methods
- story structure
### Deleted
- old tools.py
- olt testtools.py

## [0.1.0] - 2019-04-10
### Added
- new Base Action
- new Base Subject
- Subject class for basic all subject
### Changed
- StoryDB to Master
- All tests with new Action and Subject
### Deleted
- Behavior
- BehavType
- old Person class (have many attr)

## [0.0.9] - 2019-04-08
### Added
- Characters count
- Insert break line
- Break symbol
- Combine description
- Dialogue mode in description
- Replaced calling tag in description
### Changed
- Omit description using a priority
### Fixed
- (Kakko, Hatena) and Maru bug
- Combine bug (vanish or each inserted break line)

## [0.0.8] - 2019-04-05
### Added
- Utility functions(assertion, print test title)
- Omit description
- Story title(episode title) inserted break line before
- Description shorter typing
### Changed
- Class and function arg type check using custom assertion
- Multi calling attribute
### Fixed
- No use comma when after symbol
- Coverage check
- Behavior REPLY lacking

## [0.0.7] - 2019-04-02
### Added
- StoryDB
- Info, Nothing
- AuxVerb
- Converted objects
- Multi object at an action
### Changed
- Refined Action
- Assertion for object types

## [0.0.6] - 2019-03-25
### Added
- New action group (scene, combi)
- negative mode
- action flags and deflags
### Changed
- output an action format
### Fixed
- error message without an action info
- error message without an object name

## [0.0.5] - 2019-03-19
### Added
- Word class
- Action's object param
- Behavior type
- Many new attribute words to Person class
- Passive mode to Action
- Language type
### Changed
- Outline test using Action
### Fixed
- Top space with a description
- Exchanged commandline action flags

## [0.0.4] - 2019-03-19
### Added
- ActionGroup class
- Master class (inherited Subject class)
### Changed
- Action class < Act class
- Story management as ActionGroup
### Deleted
- Story class
- Episode class
- Scene class

## [0.0.3] - 2019-03-18
### Added
- Github issue template
- Github pull request template
- BaseAction class
- Story class
- Episode class
- Scene class
- story building method
- option parser
- output as action infos
### Changed
- Act's verb without a particle
### Fixed
- Failed to equal sentences in testtools

## [0.0.2] - 2019-03-11
### Added
- Act class to add a new attr "behavior"
- Behavior enum types (from major english verbs)
- Subject class for using act's subject base
### Changed
- Person, Stage, Item and DayTime class based Subject
- Story check test completely 5w1h.
### Deleted
- Example story and test.
- ActType(MUST, DONE)
- Must and Done act (instead to an act behavior).

## [0.0.1] - 2019-03-08
### Added
- This CHANGELOG file to hopefully serve as an evolving example of a standardized open source project CHANGELOG.
- README one line implemented.
- Basic classes to build a story.
- Test suites for basic features.
- Example story as usage.
- Output story as markdown.

[Unreleased]: https://github.com/nagisc007/storybuilder/compare/v0.5.1-4...HEAD
[0.5.1-4]: https://github.com/nagisc007/storybuilder/releases/v0.5.1-4
[0.5.1-3]: https://github.com/nagisc007/storybuilder/releases/v0.5.1-3
[0.5.1-2]: https://github.com/nagisc007/storybuilder/releases/v0.5.1-2
[0.5.1-1]: https://github.com/nagisc007/storybuilder/releases/v0.5.1-1
[0.5.1]: https://github.com/nagisc007/storybuilder/releases/v0.5.1
[0.5.0]: https://github.com/nagisc007/storybuilder/releases/v0.5.0
[0.4.5-7]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-7
[0.4.5-6]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-6
[0.4.5-5]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-5
[0.4.5-4]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-4
[0.4.5-3]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-3
[0.4.5-2]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-2
[0.4.5-1]: https://github.com/nagisc007/storybuilder/releases/v0.4.5-1
[0.4.5]: https://github.com/nagisc007/storybuilder/releases/v0.4.5
[0.4.4-5]: https://github.com/nagisc007/storybuilder/releases/v0.4.4-5
[0.4.4-4]: https://github.com/nagisc007/storybuilder/releases/v0.4.4-4
[0.4.4-3]: https://github.com/nagisc007/storybuilder/releases/v0.4.4-3
[0.4.4-2]: https://github.com/nagisc007/storybuilder/releases/v0.4.4-2
[0.4.4-1]: https://github.com/nagisc007/storybuilder/releases/v0.4.4-1
[0.4.4]: https://github.com/nagisc007/storybuilder/releases/v0.4.4
[0.4.3-33]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-33
[0.4.3-32]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-32
[0.4.3-31]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-31
[0.4.3-30]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-30
[0.4.3-29]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-29
[0.4.3-28]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-28
[0.4.3-27]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-27
[0.4.3-26]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-26
[0.4.3-25]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-25
[0.4.3-24]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-24
[0.4.3-23]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-23
[0.4.3-22]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-22
[0.4.3-21]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-21
[0.4.3-20]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-20
[0.4.3-19]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-19
[0.4.3-18]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-18
[0.4.3-17]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-17
[0.4.3-16]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-16
[0.4.3-15]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-15
[0.4.3-14]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-14
[0.4.3-13]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-13
[0.4.3-12]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-12
[0.4.3-11]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-11
[0.4.3-10]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-10
[0.4.3-9]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-9
[0.4.3-8]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-8
[0.4.3-7]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-7
[0.4.3-6]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-6
[0.4.3-5]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-5
[0.4.3-4]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-4
[0.4.3-3]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-3
[0.4.3-2]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-2
[0.4.3-1]: https://github.com/nagisc007/storybuilder/releases/v0.4.3-1
[0.4.3]: https://github.com/nagisc007/storybuilder/releases/v0.4.3
[0.4.2]: https://github.com/nagisc007/storybuilder/releases/v0.4.2
[0.3.2]: https://github.com/nagisc007/storybuilder/releases/v0.3.2
[0.3.1]: https://github.com/nagisc007/storybuilder/releases/v0.3.1
[0.3.0]: https://github.com/nagisc007/storybuilder/releases/v0.3.0
[0.2.10]: https://github.com/nagisc007/storybuilder/releases/v0.2.10
[0.2.9]: https://github.com/nagisc007/storybuilder/releases/v0.2.9
[0.2.1]: https://github.com/nagisc007/storybuilder/releases/v0.2.1
[0.2.0]: https://github.com/nagisc007/storybuilder/releases/v0.2.0
[0.1.0]: https://github.com/nagisc007/storybuilder/releases/v0.1.0
[0.0.9]: https://github.com/nagisc007/storybuilder/releases/v0.0.9
[0.0.8]: https://github.com/nagisc007/storybuilder/releases/v0.0.8
[0.0.7]: https://github.com/nagisc007/storybuilder/releases/v0.0.7
[0.0.6]: https://github.com/nagisc007/storybuilder/releases/v0.0.6
[0.0.5]: https://github.com/nagisc007/storybuilder/releases/v0.0.5
[0.0.4]: https://github.com/nagisc007/storybuilder/releases/v0.0.4
[0.0.3]: https://github.com/nagisc007/storybuilder/releases/v0.0.3
[0.0.2]: https://github.com/nagisc007/storybuilder/releases/v0.0.2
[0.0.1]: https://github.com/nagisc007/storybuilder/releases/v0.0.1
