# -*- coding: utf-8 -*-
from ndd_tools.data_models import LoggerConfig
from pydantic import ValidationError


def test_logger_config_logger_custom_field_type():
    import logging

    c = LoggerConfig(logger=logging.getLogger())
    assert c
    assert isinstance(c.logger, logging.Logger)


def test_logger_config_level_validator():
    import logging

    # case input level is true
    c = LoggerConfig(level=logging.DEBUG)
    assert c
    assert c.level == logging.DEBUG

    # case input level is false
    try:
        c1 = LoggerConfig(level=100)
        c1.level
    except ValidationError:
        # c1 must raise exceptio
        assert True
    except Exception:
        # other exception is error
        assert False

    # case no input level
    c2 = LoggerConfig()
    assert c2.level is None
