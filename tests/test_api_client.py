# -*- coding: utf-8 -*-
from ndd_tools.api_client import ApiClient
from ndd_tools.data_models import LoggerConfig
from ndd_tools.constants import KW_LOGGER_CONFIG
import os


def test_api_client():
    client = ApiClient(
        os.path.join(
            os.getcwd(),
            'example',
            'api_params.json'
        )
    )

    data = client.make_request('example1')
    assert data


def test_api_client_load_config_error():
    try:
        client = ApiClient(
            os.path.join(
                os.getcwd(),
                'example',
                'error.json'
            )
        )
    except FileNotFoundError:
        assert True
    except Exception:
        assert False


def test_api_client_with_debug():
    logger_config = LoggerConfig(enable_debug=True)
    client = ApiClient(
        os.path.join(
            os.getcwd(),
            'example',
            'api_params.json'
        ),
        **{KW_LOGGER_CONFIG: logger_config}
    )
    client.debug("hello world")
    # print(client.logger_config)
    data = client.make_request('example1')
    assert data
