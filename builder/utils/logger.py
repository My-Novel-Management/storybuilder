# -*- coding: utf-8 -*-
'''
Logger object
=============
'''

from __future__ import annotations

__all__ = ('MyLogger',)

import argparse
import logging


class MyLogger(logging.Logger):
    ''' MyLogger class, that writes a log to a file.

    Attributes:
        name(str): logger name.
        sh_format(str=None): stream format.
        fh_format(str=None): file format.
    '''

    _file_handler = None
    _shared_log_level = logging.DEBUG
    _shared_logger = []
    _LOG_DIR = 'logs'

    def __init__(self, name: str, sh_format: str=None, fh_format: str=None):
        super().__init__(name)
        self._log_level = logging.DEBUG
        self._sh_formatter = logging.Formatter(sh_format if sh_format else '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._fh_formatter = logging.Formatter(fh_format if fh_format else '%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')

    @staticmethod
    def get_logger(modname: str=__name__, sh_format: str=None, fh_format: str=None,
            is_specific: bool=False) -> MyLogger:
        ''' Get MyLogger class same instance.
        '''
        logger = MyLogger(modname, sh_format, fh_format)
        logger._set_default()
        if not is_specific:
            MyLogger._shared_logger.append(logger)
        return logger

    def reset_logger(self, options: argparse.Namespace) -> None:
        if options.log or options.debug:
            opt_log = options.log if options.log else 'debug'
            level = 'debug' if options.debug else opt_log
            self.set_shared_level(level)
            MyLogger.reset_level()
            self.debug(f'LOGGER: reset level: {self.level}')

    @classmethod
    def reset_level(cls, level: str='') -> None:
        ''' Reset shared log level
        '''
        for logger in cls._shared_logger:
            logger.set_level(level)

    def set_level(self, level: str='') -> None:
        ''' Set logger level.
        '''
        if level:
            self._log_level = self._get_log_level(level)
            self.setLevel(self._log_level)
        else:
            self.setLevel(MyLogger._shared_log_level)

    def set_shared_level(self, level: str) -> None:
        ''' Set shared log level.
        '''
        MyLogger._shared_log_level = self._get_log_level(level)

    def set_stream_handler(self) -> None:
        ''' Set stream handler.
        '''
        sh = logging.StreamHandler()
        sh.setLevel(self._log_level)
        sh.setFormatter(self._sh_formatter)
        self.addHandler(sh)

    def set_file_handler(self, fname: str=None) -> None:
        ''' Set file handler.
        '''
        fh = None
        if not fname and MyLogger._file_handler:
            fh = MyLogger._file_handler
        elif fname:
            import os
            if not os.path.isdir(MyLogger._LOG_DIR):
                os.makedirs(MyLogger._LOG_DIR)
            filepath = os.path.join(MyLogger._LOG_DIR,
                    f'{fname}.log')
            fh = logging.FileHandler(filepath)
            fh.setLevel(self._log_level)
            fh.setFormatter(self._fh_formatter)
            MyLogger._file_handler = fh
        else:
            raise ValueError('Cannot filename for log file handler!')
        self.addHandler(fh)

    def set_stream_formatter(self, fmt: str) -> None:
        ''' Set stream formatter.
        '''
        self._sh_formatter = fmt

    def set_file_formatter(self, fmt: str) -> None:
        ''' Set file formatter.
        '''
        self._fh_formatter = fmt

    #
    # private
    #

    def _get_log_level(self, level: str) -> int:
        _lvl = level.lower()
        if _lvl in ('d', 'debug'):
            return logging.DEBUG
        elif _lvl in ('i', 'info'):
            return logging.INFO
        elif _lvl in ('w', 'warning', 'warn'):
            return logging.WARNING
        elif _lvl in ('e', 'error'):
            return logging.ERROR
        elif _lvl in ('c', 'critical'):
            return logging.CRITICAL
        else:
            return logging.DEBUG

    def _set_default(self):
        res = True
        self.set_level()
        self.set_stream_handler()
        return res
