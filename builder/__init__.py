# The init file is for storybuilder, that a story building manager on console.
# License: MIT License, @see the file 'LICENSE' for details.
'''
StoryBuilder framework
======================

StoryBuilder is a library for developing story contents. the terms of
the `MIT License <https://en.wikipedia.org/wiki/MIT_License>`_.
'''
import sys


MAJOR = 0
MINOR = 6
MICRO = 2
FEATURE = 0

#
# Information
#

__TITLE__ = 'StoryBuilder'
__LICENSE__ = 'MIT'
__VERSION__ = f"{MAJOR}.{MINOR}.{MICRO}-{FEATURE}" if int(FEATURE) else f"{MAJOR}.{MINOR}.{MICRO}"
__AUTHOR__ = __maintainer__ = 'N.T.Works'
__EMAIL__ = 'nagisc007@yahoo.co.jp'
__DESC__ = 'Story builder is a library for developing story contents.'


#
# CONSTANTS
#

__DEFAULT_LOG_LEVEL__ = 'warning'
__PRIORITY_DEFAULT__ = 5
__PRIORITY_MAX__ = 10
__PRIORITY_MIN__ = 0

VERSION_MSG = (
        'StoryBuilder: version: v{0}'.format(__VERSION__),
        'Python: version: {0}'.format(' '.join(line.strip() for line in sys.version.splitlines())),
        )

#
# LOGGER
#
import datetime
from builder.utils.logger import MyLogger

LOG = MyLogger.get_logger(__TITLE__)
LOG.set_file_handler(f'{datetime.date.today()}')
LOG.set_shared_level(__DEFAULT_LOG_LEVEL__)

