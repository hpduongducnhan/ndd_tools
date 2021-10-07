import os
from ndd_tools.regex_executor import RegexExecutor
from ndd_tools.schemas import RegexExecutorConfig
import yaml

EXPECT_OUTPUT_A = "hello, success A"
EXPECT_OUTPUT_B = "hello, success B"
EXPECT_OUTPUT_C = "hello, success C"
EXPECT_OUTPUT_D = "hello, success D"
access_paths_1 = ["services", '[...]', "output" ]
input_data_1 = {
    "services": [
        {
            "output": EXPECT_OUTPUT_A
        },
        {
            'output': EXPECT_OUTPUT_B
        },
        {
            'output': EXPECT_OUTPUT_C
        }
    ]
}
access_paths_2 = ['[...]', 'services', '[...]', 'output']
input_data_2 = [
    {
        "services": [
            {
                "output": EXPECT_OUTPUT_A
            },
            {
                'output': EXPECT_OUTPUT_B
            }
        ]
    },
    {
        "services": [
            {
                "output": EXPECT_OUTPUT_C
            },
            {
                'output': EXPECT_OUTPUT_D
            }
        ]
    }
]
access_paths_3 = ['[...]', 'services', '[...]', 'x', '[...]', 'output']
input_data_3 = [
    {
        "services": [
            {
                'x': [
                    {"output": EXPECT_OUTPUT_A},
                    {"output": EXPECT_OUTPUT_B}
                ]
            }, 
            {
                'x': [
                    {"output": EXPECT_OUTPUT_C}
                ]
            }
        ]
    },
    {
        "services": [
            {
                'x': [
                    {"output": EXPECT_OUTPUT_A},
                    {"output": EXPECT_OUTPUT_B}
                ]
            }, 
            {
                'x': [
                    {"output": EXPECT_OUTPUT_C}
                ]
            }
        ]
    }
]

def test_create_instance_by_set_config():
    file_path = os.path.join(os.getcwd(), 'example', 'boring_regex_config.yml')
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        # print(data)
        config = RegexExecutorConfig.parse_obj(data)
    assert config
    assert isinstance(config, RegexExecutorConfig)
    ins = RegexExecutor()
    ins.set_config(config)
    assert isinstance(ins.config, RegexExecutorConfig)
    return ins

def test_create_intance_by_set_config_file_path() -> RegexExecutor:
    ins = RegexExecutor()
    ins.set_config_file_path(
        os.path.join(os.getcwd(), 'example', 'boring_regex_config.yml')
    )
    return ins


def test_create_instance() -> RegexExecutor:
    ins = RegexExecutor()
    ins.set_config_file_path(
        os.path.join(os.getcwd(), 'example', 'boring_regex_config.yml')
    )
    return ins


def test_build_paths_case_normal():
    ins = test_create_instance_by_set_config()
    access_paths = access_paths_1
    input_data = input_data_1
    paths = ins.build_field_paths(access_paths, input_data)
    assert len(paths) == 3
    assert paths == [
        ['services', 0, 'output'],
        ['services', 1, 'output'],
        ['services', 2, 'output']
    ]
    
def test_build_paths_case_nested():
    ins = test_create_instance_by_set_config()
    access_paths = access_paths_2
    input_data = input_data_2
    paths = ins.build_field_paths(access_paths, input_data)
    assert len(paths) == 4
    assert paths == [
        [0, 'services', 0, 'output'],
        [0, 'services', 1, 'output'],
        [1, 'services', 0, 'output'],
        [1, 'services', 1, 'output']
    ]

def test_build_paths_case_complicatly_nested():
    ins = test_create_instance_by_set_config()
    access_paths = access_paths_3
    input_data = input_data_3
    paths = ins.build_field_paths(access_paths, input_data)
    assert len(paths) == 6
    assert paths == [
        [0, 'services', 0, 'x', 0, 'output'],
        [0, 'services', 0, 'x', 1, 'output'],
        [0, 'services', 1, 'x', 0, 'output'],
        [1, 'services', 0, 'x', 0, 'output'],
        [1, 'services', 0, 'x', 1, 'output'],
        [1, 'services', 1, 'x', 0, 'output']
    ]

def test_find_field_values_case_one_value():
    EXPECT_OUTPUT = "hello, success"
    access_path = ['services', 0, 'output']
    input_data = {
        "services": [
            {
                "output": EXPECT_OUTPUT
            }
        ]
    }
    ins = test_create_instance_by_set_config()
    output = ins.find_field_values(access_path, input_data)
    assert output == [EXPECT_OUTPUT]


def test_find_field_values_case_array_values():
    EXPECT_OUTPUT_A = "hello, success"
    EXPECT_OUTPUT_B = "hello, success"
    access_path = ['services', '[...]', 'output']
    input_data = {
        "services": [
            {
                "output": EXPECT_OUTPUT_A
            },
            {
                'output': EXPECT_OUTPUT_B
            }
        ]
    }
    ins = test_create_instance_by_set_config()
    output = ins.find_field_values(access_path, input_data)
    assert output == [EXPECT_OUTPUT_A, EXPECT_OUTPUT_B]


def test_find_field_values_case_nested_array_values():
    EXPECT_OUTPUT_A = "hello, success A"
    EXPECT_OUTPUT_B = "hello, success B"
    EXPECT_OUTPUT_C = "hello, success C"
    access_path = ['services', '[...]', 'x', '[...]', 'output']
    input_data = {
        "services": [
            {
                'x': [
                    {"output": EXPECT_OUTPUT_A},
                    {"output": EXPECT_OUTPUT_B}
                ]
            }, 
            {
                'x': [
                    {"output": EXPECT_OUTPUT_C}
                ]
            }
        ]
    }
    ins = test_create_instance_by_set_config()
    output = ins.find_field_values(access_path, input_data)
    assert output == [EXPECT_OUTPUT_A, EXPECT_OUTPUT_B, EXPECT_OUTPUT_C]
