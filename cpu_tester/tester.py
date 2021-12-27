import json
import os
import random
import sys

from pycpu.instruction import Instruction
from pycpu.mips.mips import MIPS
from pycpu.mips.tests.programs_generator import ProgramGenerator
from pycpu.mips.tests.verilog_api import VerilogApi

DEFAULT_CONFIG = {
    'cpu_test_path': './cpu/cpu_test.v',
    'cpu_folder': './cpu',
    'max_instructions': 200,
    'instructions_file': 'instructions.dat',
    'tests': 10000,
    'memory_cells': 10,
    'iverilog_flags': '-g2012',
    'test_build_folder': 'test_build_folder',
    'registers_range': (1, 10),
    'fails_folder': './fails',
}


def save_failed_program(instructions: [Instruction], fail_folder):
    if not os.path.isdir(fail_folder):
        os.mkdir(fail_folder)

    _bin = '\n'.join(map(lambda i: i.binary(), instructions))
    _asm = '\n'.join(map(lambda i: i.asm(), instructions))

    tag = random.randint(0, 10000000)

    # dumping binaries
    with open(os.path.join(fail_folder, f'{tag}_bin'), 'w') as f:
        f.write(_bin)
    # dumping asm
    with open(os.path.join(fail_folder, f'{tag}_asm'), 'w') as f:
        f.write(_asm)
    return tag


def read_config(config_path):
    _config = {}
    _file_data = None
    if os.path.isfile(config_path):
        _file_data = json.load(config_path)
    for key in DEFAULT_CONFIG:
        if _file_data is not None:
            if key in _file_data:
                _config[key] = _file_data[key]
                continue
        _config[key] = DEFAULT_CONFIG[key]
    return _config


if __name__ == '__main__':
    args = sys.argv[1:]
    config_path = 'config.json'
    if len(args) > 0:
        config_path = args[0]

    config = read_config(config_path)

    # initializing entities
    cpu = MIPS(
        mem_size=config['memory_cells'],
        reg_cnt=32,
    )

    verilog = VerilogApi(
        test_path=config['cpu_test_path'],
        build_folder_path=config['test_build_folder'],
        iverilog_build_flags=f'{config["iverilog_flags"]} -I {config["cpu_folder"]}',
        max_instructions=config['max_instructions'],
        instructions_file_path=config['instructions_file']
    )

    generator = ProgramGenerator(
        memory_cells=config['memory_cells'],
        amount=config['max_instructions'] - 1,
        reg_range=config['registers_range']
    )

    passed = 0
    failed = 0
    total = config['tests']
    log_breakpoint = 100
    used_memory_cells = config['memory_cells']

    for i in range(total):
        if i % log_breakpoint == log_breakpoint - 1:
            print(f'total: {total} passed: {passed} failed: {failed}')

        instructions = generator.generate()
        try:
            cpu.reset()
            cpu.set_instructions(instructions)
            cpu.run()
        except Exception as ex:
            print('error occurred while running cpu tests:')
            print(ex)
            print('-' * 27)
            print('Input something to continue:')
            input()
            continue

        try:
            verilog_memory = verilog.run(instructions)
        except Exception as ex:
            print('error occurred while running cpu tests:')
            print(ex)
            print('-' * 27)
            print('Input something to continue:')
            input()
            continue

        for i in range(used_memory_cells):
            cpu_cell = cpu.read_mem(i)
            verilog_cell = verilog_memory[i]
            if cpu_cell != verilog_cell:
                failed += 1
                tag = save_failed_program(instructions, config['fails_folder'])
                print(f'failure! tag={tag}')
                print('verilog memory:', verilog_memory)
                print('cpu memory:', cpu.memory)
                break
        else:
            passed += 1

