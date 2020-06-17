# -*- coding: utf-8 -*-
'''
Logger object
=============
'''

from __future__ import annotations

__all__ = ('MyLogger',)

import logging


class MyLogger(logging.Logger):
    ''' MyLogger class, that writes a log to a file.

    Attributes:
        name(str): logger name.
        sh_format(str=None): stream format.
        fh_format(str=None): file format.
    '''

    _file_handler = None
    _LOG_DIR = 'logs'

    def __init__(self, name: str, sh_format: str=None, fh_format: str=None):
        super().__init__(name)
        self._log_level = logging.DEBUG
        self._sh_formatter = logging.Formatter(sh_format if sh_format else '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._fh_formatter = logging.Formatter(fh_format if fh_format else '%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')

    @staticmethod
    def get_logger(modname: str=__name__, sh_format: str=None, fh_format: str=None) -> MyLogger:
        ''' Get MyLogger class same instance.
        '''
        logger = MyLogger(modname, sh_format, fh_format)
        logger._set_default()
        return logger

    def set_level(self, level: str='debug') -> None:
        ''' Set logger level.
        '''
        _lvl = level.lower()
        if _lvl in ('d', 'debug'):
            self._log_level = logging.DEBUG
        elif _lvl in ('i', 'info'):
            self._log_level = logging.INFO
        elif _lvl in ('w', 'warning', 'warn'):
            self._log_level = logging.WARNING
        elif _lvl in ('e', 'error'):
            self._log_level = logging.ERROR
        elif _lvl in ('c', 'critical'):
            self._log_level = logging.CRITICAL
        else:
            # TODO: 設定ミスになる場合にデフォルトを当てるかエラー出すか
            pass
        self.setLevel(self._log_level)

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

    def _set_default(self):
        res = True
        self.set_level()
        self.set_stream_handler()
        return res
