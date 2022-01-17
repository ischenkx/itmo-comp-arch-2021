import json
import os

DEFAULT_CONFIG = {
    'cpu_test_path': './cpu/cpu_test.v',
    'cpu_folder': './cpu',
    'max_instructions': 200,
    'instructions_folder': 'instructions_tmp_folder',
    'tests': 10000,
    'memory_cells': 10,
    'iverilog_flags': '-g2012',
    'test_build_folder': 'test_build_folder',
    'registers_range': (1, 10),
    'fails_folder': './fails',
    'workers': 4,
    'time_out': 5000,
    'memory_array_name': None,
    'registers_array_name': None,
    'instructions_array_name': None,
}


class Config(object):

    @staticmethod
    def from_file(config_path):
        _config = {}
        _file_data = None
        if os.path.isfile(config_path):
            with open(config_path) as f:
                _file_data = json.load(f)
        for key in DEFAULT_CONFIG:
            if _file_data is not None:
                if key in _file_data:
                    _config[key] = _file_data[key]
                    continue
            _config[key] = DEFAULT_CONFIG[key]
        return Config(**_config)

    def __init__(self,
                 cpu_test_path,
                 cpu_folder,
                 max_instructions,
                 instructions_folder,
                 tests,
                 memory_cells,
                 iverilog_flags,
                 test_build_folder,
                 registers_range,
                 fails_folder,
                 time_out,
                 workers,
                 memory_array_name,
                 registers_array_name,
                 instructions_array_name
    ):
        self.cpu_test_path = cpu_test_path
        self.cpu_folder = cpu_folder
        self.max_instructions = max_instructions
        self.instructions_folder = instructions_folder
        self.tests = tests
        self.memory_cells = memory_cells
        self.iverilog_flags = iverilog_flags
        self.test_build_folder = test_build_folder
        self.registers_range = registers_range
        self.fails_folder = fails_folder
        self.time_out = time_out
        self.workers = workers
        self.memory_array_name = memory_array_name
        self.registers_array_name = registers_array_name
        self.instructions_array_name = instructions_array_name

