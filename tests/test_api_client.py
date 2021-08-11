# -*- coding: utf-8 -*-
from ndd_tools.api_client import ApiClient
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
    client = ApiClient(
        os.path.join(
            os.getcwd(),
            'example',
            'api_params.json'
        ),
        enable_debug=True
    )

    data = client.make_request('example1')
    assert data
