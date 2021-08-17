# -*- coding: utf-8 -*-
import os
from typing import List
from tests.test_api_client import test_api_client_with_debug
from tests.test_logger_mixin import test_logger_mixin_propagate
from ndd_tools import LoggerConfig, data_models
from ndd_tools.boring_regex import BoringRegex, BRConfigModel


def test_boring_regex():
    x = BoringRegex(
        BRConfigModel(file_path=os.path.join(os.getcwd(), 'example', 'boring_regex_config.yml'))
    )
    x.run(
        {
            "icon": "switch",
            "state": "up",
            "summary": {
                "ok": "1",
                "handled": "1",
                "computed_state": "ok",
                "unhandled": "0",
                "total": "1"
            },
            "unhandled": "0",
            "max_check_attempts": "2",
            "num_interfaces": "0",
            "state_duration": "23802181",
            "services": [
                {
                    "max_check_attempts": "2",
                    "markdown": "0",
                    "state_duration": "2395895",
                    "state_type": "hard",
                    "name": "check_sw_huawei_temp",
                    "current_check_attempt": "1",
                    "output": "OK - TEMP: [T1: 27C]. [T2: 28C]. [T3: 28C]. [T4: 33C]. [T5: 32C]. [T6: 34C]. [T9: 33C]. [T10: 26C]. [T11: 26C]. [T12: 25C]. [T13: 29C]. [T14: 29C]. [T15: 27C]. [T18: 28C].",
                    "state": "ok",
                    "service_object_id": "10131",
                    "unhandled": "0",
                    "downtime": "0",
                    "last_check": "1629106013",
                    "perfdata_available": "0"
                },
                {
                    "max_check_attempts": "2",
                    "markdown": "0",
                    "state_duration": "2395895",
                    "state_type": "hard",
                    "name": "check_sw_huawei_temp",
                    "current_check_attempt": "1",
                    "output": "OK - TEMP: [T1: 27C]. [T2: 28C]. [T3: 28C]. [T4: 33C]. [T5: 32C]. [T6: 34C]. [T9: 33C]. [T10: 26C]. [T11: 26C]. [T12: 25C]. [T13: 29C]. [T14: 29C]. [T15: 27C]. [T18: 28C].",
                    "state": "ok",
                    "service_object_id": "10131",
                    "unhandled": "0",
                    "downtime": "0",
                    "last_check": "1629106013",
                    "perfdata_available": "0"
                }
            ],
            "name": "BTHT1-CE501040HCMP00501HW24-11.51.42.21",
            "state_type": "hard",
            "current_check_attempt": "1",
            "output": "OK - 11.51.42.21: rta 8.803ms, lost 0%",
            "num_services": "18",
            "downtime": "0",
            "last_check": "1629104908",
            "alias": "Ho Chi Minh_undefined_INF Huawei S6324"
        },
        'FTS_1220_check_sw_huawei_temp'
    )


if __name__ == '__main__':
    test_boring_regex()
