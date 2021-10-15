# before run this script
# pip install ndd-tools 
#

import os
import json
import sys
from ndd_tools import RegexExecutor, RegexExecutorConfig, load_regex_config_file


def run(config_file, data_file: str):
    client = RegexExecutor()
    config: RegexExecutorConfig = load_regex_config_file(config_file)
    client.set_config(config)

    # load data example: FTS_1214_check_sw_huawei_temp.json 
    # data_file is name of config regex 
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    result = []
    for item in data['list']:
        response = client.run(item, data_file.replace('.json', ''))
        # print('----------------------------------------')
        # print(f'item -> {item}')
        print(f'response -> {response}')
        print(response.get('temp'))
        result.append(response.dict())

    # save to file

    with open('regex_result.json', 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    run(
        os.path.join(os.getcwd(), 'example', 'boring_regex_config.yml'),
        'FTS_1214_check_sw_huawei_temp.json'
    )