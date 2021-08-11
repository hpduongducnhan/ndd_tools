# -*- coding: utf-8 -*-
import logging
import sys
import os
import uuid
from datetime import datetime
from typing import List
from .constants import LOGGER, LOGGER_CONFIG, LOGGER_FORMATTER
from .data_models import LoggerConfig
from .others import create_directory


def find_logger_handler_stream_stdout(handlers: List[logging.Handler]):
    found_handler = None
    for handler in handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream is sys.stdout:
            found_handler = handler
            found_handler.close()
            return found_handler


class LoggerMixin:
    def set_logger_debug_mode(self, mode: bool) -> None:
        if mode:
            self.set_logger_level(logging.DEBUG)
            if not find_logger_handler_stream_stdout(self.logger.handlers):
                self.logger.addHandler(logging.StreamHandler(sys.stdout))
            self.debug('debug_mode on')
        else:
            self.debug('debug_mode off')
            self.set_logger_level(logging.INFO)
            deleted_handler = find_logger_handler_stream_stdout(self.logger.handlers)
            if deleted_handler:
                self.logger.handlers.remove(deleted_handler)

    def set_logger_level(self, level: int):
        if level in [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]:
            self.logger.setLevel(level)

    def add_logger_file_handler(self, fpath: str, fname: str, formatter: str = LOGGER_FORMATTER):
        self.logger.addHandler(
            self.create_logger_file_handler(fpath, fname, formatter)
        )

    def create_logger_file_handler(self, fpath: str, fname: str, formatter: str):
        fhandler = logging.FileHandler(
            os.path.join(fpath, fname)
        )
        fhandler.setFormatter(logging.Formatter(formatter))
        return fhandler

    def set_logger_up(self, config: LoggerConfig = None) -> None:
        # default config
        # logger = logging.getLogger(<class_name>)
        # name = root;  level = info;
        # propagate = unique_logger = enable_log_file = enable_debug = False
        # log_file_name = self.__class__.__name
        # unique_name = <log_file_name>_<uuidv4>
        # log_file_path = ~<project>/log/default/<log_file_name>.log
        if not config:
            config = LoggerConfig()

        # inherit logger
        if config.logger:
            config.name = config.logger.name
            config.level = config.logger.level
            setattr(self, LOGGER_CONFIG, config)
            setattr(self, LOGGER, config.logger)
            return
        # set default logger level
        if not config.level:
            config.level = logging.INFO
        # set default logger name follow class name
        if not config.name:
            config.name = self.__class__.__name__
        # set default logger file name by adding string date and follow logger name
        if not config.log_file_name:
            config.log_file_name = f'{datetime.now().strftime("%Y%m%d")}_{config.name}.log'
        # set default logger file path
        if not config.log_file_path:
            config.log_file_path = os.path.join(os.getcwd(), 'log', 'default')
        # create logger
        _logger = None
        if config.unique_logger:
            # create unique logger
            if not config.unique_name:
                config.unique_name = config.name + "_" + str(uuid.uuid4())
            _logger = logging.getLogger(config.unique_name)
            _logger.setLevel(config.level)
        elif config.name in logging.Logger.manager.loggerDict.keys():
            # check exist logger in system
            _logger = logging.getLogger(config.name)
        else:
            _logger = logging.getLogger(config.name)
            _logger.setLevel(config.level)
        # check if need add file handler
        if config.enable_log_file:
            create_directory(config.log_file_path)
            _logger.addHandler(
                self.create_logger_file_handler(
                    config.log_file_path,
                    config.log_file_name,
                    config.formatter
                )
            )
        # enable debug mode
        if config.enable_debug:
            self.set_logger_debug_mode(True)
        # add instance attribute
        config.logger = _logger
        setattr(self, LOGGER_CONFIG, config)
        setattr(self, LOGGER, _logger)

    @property   # getter
    def logger_config(self):
        if not hasattr(self, LOGGER_CONFIG):
            return LoggerConfig()
        return getattr(self, LOGGER_CONFIG)

    @property   # getter
    def logger(self) -> logging.Logger:
        if not hasattr(self, LOGGER):
            # setup with default logger
            # if you need setup logger, please use set_logger_up method
            self.set_logger_up(LoggerConfig())
        return getattr(self, LOGGER)

    @property   # getter
    def logger_name(self) -> str:
        return self.logger.name

    def _format_log_msg(self, msg) -> str:
        return f'{self.__class__.__name__}: {msg}'

    def debug(self, msg: str):
        self.logger.debug(self._format_log_msg(msg))

    def info(self, msg: str):
        self.logger.info(self._format_log_msg(msg))

    def warn(self, msg: str):
        self.logger.warn(self._format_log_msg(msg))

    def error(self, msg: str):
        self.logger.error(self._format_log_msg(msg))

    def critical(self, msg: str):
        self.logger.critical(self._format_log_msg(msg))

    def stack_trace(self, msg: str, error: any):
        self.error(msg)
        self.logger.exception(error)
