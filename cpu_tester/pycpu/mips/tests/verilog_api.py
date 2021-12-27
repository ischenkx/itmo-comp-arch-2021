import os
import random
import subprocess
import shutil
from pycpu.instruction import Instruction
from pycpu.mips.util import twos_comp


def _expand_array(arr, size):
    if len(arr) >= size:
        return arr
    arr.extend([0] * (size - len(arr)))


class VerilogApi(object):
    def __init__(self,
                 test_path,
                 build_folder_path,
                 iverilog_build_flags,
                 max_instructions,
                 instructions_file_path
                 ):

        self.test_path = test_path
        self._instructions_file_path = instructions_file_path
        self._build_folder_path = build_folder_path
        self._iverilog_build_flags = iverilog_build_flags
        self._max_instructions = max_instructions
        self._build_file_name = str(random.randint(1, 1 << 30))
        self._init_build_folder()
        self._compile_tests()

    def _get_build_folder_path(self):
        return os.path.join(os.getcwd(), self._build_folder_path)

    def _get_build_file_path(self):
        return os.path.join(self._get_build_folder_path(), self._build_file_name)

    def _init_build_folder(self):
        if not os.path.isdir(self._get_build_folder_path()):
            os.mkdir(self._get_build_folder_path())

    def _compile_tests(self):
        subprocess.check_output(
            f'iverilog -o {self._get_build_file_path()} {self._iverilog_build_flags} {self.test_path}'
        )

    def _write_instructions(self, instructions: [Instruction]):
        if len(instructions) >= self._max_instructions:
            print('WARNING: can\'t safely reserve a cell for a breakpoint!')
            instructions = instructions[:self._max_instructions - 1]
        lines = '\n'.join(map(lambda x: x.binary(), instructions))
        with open(self._instructions_file_path, 'w') as f:
            f.write(lines)
            # breakpoint
            f.write('\n' + '0' * 32)

    def _decode_tests_output(self, out):
        memory = []
        memory_reading = False
        out = out.decode(encoding='utf-8')
        lines = out.split(os.linesep)
        for line in lines:
            line = line.strip()
            if line == 'MEMORY_DUMP_BEGIN':
                memory_reading = True
            elif line == 'MEMORY_DUMP_END':
                memory_reading = False
            elif line == 'FINISH':
                break
            else:
                if memory_reading:
                    parts = list(filter(lambda x: len(x) > 0, line.split(' ')))
                    index, value = int(parts[0]), twos_comp(int(parts[1], 2), 32)
                    _expand_array(memory, index + 1)
                    memory[index] = value
        return memory

    def close(self):
        shutil.rmtree(os.path.join(os.getcwd(), self._build_folder_path), ignore_errors=True)

    def run(self, instructions: [Instruction]):
        self._write_instructions(instructions)
        command = f'vvp {self._get_build_file_path()}'
        output = subprocess.check_output(command)
        return self._decode_tests_output(output)
