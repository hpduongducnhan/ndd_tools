# -*- coding: utf-8 -*-
import logging
import os
import sys
from ndd_tools.logger_mixin import LoggerMixin
from ndd_tools.data_models import LoggerConfig
from ndd_tools.constants import LOGGER_CONFIG


class Example:
    pass


def test_logger_mixin_default_config():
    class X(Example, LoggerMixin):
        def __init__(self) -> None:
            self.set_logger_up()
            super().__init__()
    x = X()
    assert isinstance(x.logger, logging.Logger)
    assert x.logger.name == 'X'
    assert x.logger.handlers == []
    # print(x.logger, x.logger.name,  x.logger.handlers)


def test_logger_mixin_inherit():
    class X(Example, LoggerMixin):
        def __init__(self) -> None:
            super().__init__()
            self.set_logger_up(LoggerConfig(logger=logging.getLogger()))

    x = X()
    assert isinstance(x.logger, logging.Logger)
    assert x.logger.name == 'root'
    assert len(x.logger.handlers) > 0
    # print(x.logger, x.logger.name,  x.logger.handlers)


def test_logger_mixin_log_to_default_file():
    # case default file
    LOG_MSG = "hello this is a test message"

    class XX(Example, LoggerMixin):
        def __init__(self) -> None:
            super().__init__()
            self.set_logger_up(LoggerConfig(enable_log_file=True))

        def get_logger_config(self) -> LoggerConfig:
            return getattr(self, LOGGER_CONFIG)

        def write_log(self):
            self.info(LOG_MSG)

    x = XX()
    x.write_log()
    log_config = x.get_logger_config()
    log_file = os.path.join(log_config.log_file_path, log_config.log_file_name)

    assert isinstance(log_config, LoggerConfig)
    assert x.logger
    assert isinstance(x.logger, logging.Logger)
    assert x.logger.name == 'XX'
    assert len(x.logger.handlers) >= 1
    assert os.path.isfile(log_file)
    with open(log_file, 'r') as f:
        file_content = f.read()
    assert LOG_MSG in file_content

    # close file
    for handler in x.logger.handlers:
        handler.close()

    # remove file
    try:
        os.remove(log_file)
    except Exception:
        pass


def test_logger_mixin_log_to_custom_file():
    # case default file
    LOG_MSG = "hello this is a test message"

    class XY(Example, LoggerMixin):
        def __init__(self) -> None:
            super().__init__()
            self.set_logger_up(
                LoggerConfig(
                    enable_log_file=True,
                    log_file_path=os.path.join(
                        os.getcwd(),
                        'custom_log'
                    )
                )
            )

        def get_logger_config(self):
            return getattr(self, LOGGER_CONFIG)

        def write_log(self):
            self.info(LOG_MSG)

    x = XY()
    x.write_log()
    log_config = x.get_logger_config()
    log_file = os.path.join(log_config.log_file_path, log_config.log_file_name)

    assert isinstance(log_config, LoggerConfig)
    assert x.logger
    assert isinstance(x.logger, logging.Logger)
    assert x.logger.name == 'XY'
    assert len(x.logger.handlers) >= 1
    assert os.path.isfile(log_file)
    with open(log_file, 'r') as f:
        file_content = f.read()
    assert LOG_MSG in file_content

    # close file
    for handler in x.logger.handlers:
        handler.close()

    # remove file
    try:
        os.remove(log_file)
        os.rmdir(log_config.log_file_path)
    except Exception:
        pass


def test_logger_mixin_debug_mode():
    class X(Example, LoggerMixin):
        def __init__(self) -> None:
            self.set_logger_up()
            super().__init__()
    x = X()
    assert isinstance(x.logger, logging.Logger)
    assert x.logger.name == 'X'
    assert x.logger.handlers == []

    # turn debug on
    x.set_logger_debug_mode(True)
    handlers = x.logger.handlers
    assert len(handlers) >= 1

    found_stream_stdout_handler = False
    for handler in handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            found_stream_stdout_handler = True
            break
    assert found_stream_stdout_handler

    # turn debug off
    x.set_logger_debug_mode(False)
    assert len(x.logger.handlers) == 0


def test_logger_mixin_get_logger_config():
    class X(Example, LoggerMixin):
        def __init__(self) -> None:
            super().__init__()
    x = X()
    assert x.logger_config
    assert isinstance(x.logger_config, LoggerConfig)