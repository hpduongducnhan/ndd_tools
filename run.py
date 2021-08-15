# -*- coding: utf-8 -*-
from tests.test_api_client import test_api_client_with_debug
from tests.test_logger_mixin import test_logger_mixin_only_one_file_handler
from ndd_tools import LoggerConfig

if __name__ == '__main__':
    test_logger_mixin_only_one_file_handler()
