import os
import random
import subprocess
import shutil
from pycpu.instruction import Instruction
from pycpu.mips.util import twos_comp

from pyverilog.vparser.parser import VerilogCodeParser
from pyverilog.vparser import ast as vast


def _expand_array(arr, size):
    if len(arr) >= size:
        return arr
    arr.extend([0] * (size - len(arr)))


class VerilogApi(object):
    class ModuleParser(object):
        def __init__(self, filename):
            self._file = filename

        def _parse_dimensions(self, dims: vast.Dimensions):
            if dims is None:
                return None
            return list(map(self._parse_width, dims.lengths))

        def _parse_width(self, w: vast.Width):
            if w is None:
                return None
            return w.msb, w.lsb

        def _parse_variable(self, node: vast.Variable):
            return {
                'name': node.name,
                'value': node.value,
                'dimensions': self._parse_dimensions(node.dimensions),
                'width': self._parse_width(node.width),
                'signed': node.signed
            }

        def _parse_declaration(self, node: vast.Decl):
            variables = []

            for item in node.list:
                if isinstance(item, vast.Variable):
                    variables.append(self._parse_variable(item))

            return variables

        def _parse_module(self, node: vast.ModuleDef):
            name = node.name
            variables = []
            for item in node.items:
                if type(item) is vast.Decl:
                    variables.extend(self._parse_declaration(item))

            return {
                'name': name,
                'vars': variables
            }

        def _parse_modules(self, node: vast.Source):
            q = [node]
            modules = {}
            while len(q) > 0:
                last = q[-1]
                q.pop()
                if type(last) is vast.ModuleDef:
                    info = self._parse_module(last)
                    modules[info['name']] = info['vars']
                q.extend(last.children())

            return modules

        def parse(self):
            tmp_file = str(random.randint(1, 100000000))
            codeparser = VerilogCodeParser(
                [self._file],
                preprocess_output=tmp_file,
                preprocess_include=None,
                preprocess_define=None,
                outputdir='.',
                debug=False
            )
            ast = codeparser.parse()
            return self._parse_modules(ast)

    def __init__(self,
                 test_path,
                 build_folder_path,
                 iverilog_build_flags,
                 cpu_files_folder,
                 max_instructions,
                 instructions_folder_path,
                 instructions_array_name,
                 registers_array_name,
                 memory_array_name
                 ):

        self.test_path = test_path
        self._cpu_files_folder = cpu_files_folder
        self._instructions_folder_path = instructions_folder_path
        self._build_folder_path = build_folder_path
        self._iverilog_build_flags = iverilog_build_flags
        self._max_instructions = max_instructions
        self._build_file_name = str(random.randint(1, 1 << 30))
        self._instructions_file_name = str(random.randint(1, 1 << 30))
        self._instructions_array_name = instructions_array_name
        self._registers_array_name = registers_array_name
        self._memory_array_name = memory_array_name
        self._init_build_folder()
        self._init_instructions_folder()
        self._compile_tests()

    def _deduce_array_names(self):
        def find_multidimensional_vars(vars):
            return list(map(lambda x: x['name'], filter(lambda x: x['dimensions'] is not None, vars)))

        def deduce_name(cur_val, modules, mod_name, default_name):
            if cur_val is not None:
                return cur_val

            deduced_name = default_name

            if mod_name in modules:
                candidates = find_multidimensional_vars(modules[mod_name])
                if len(candidates) > 0:
                    if len(candidates) > 1:
                        print(
                            f'[ERROR] failed to deduce the name of the \'{mod_name}\' array! too many candidates: {candidates}'
                        )

                    else:
                        deduced_name = candidates[0]
            print(f'[LOG] deduced \'{mod_name}\' array name: {deduced_name}')
            return deduced_name

        memory_module_path = os.path.join(self._cpu_files_folder, 'memory.v')
        registers_module_path = os.path.join(self._cpu_files_folder, 'register_file.v')
        mem_modules = VerilogApi.ModuleParser(memory_module_path).parse()
        reg_modules = VerilogApi.ModuleParser(registers_module_path).parse()

        self._registers_array_name = deduce_name(
            self._registers_array_name,
            reg_modules,
            'register_file',
            'registers'
        )

        self._memory_array_name = deduce_name(
            self._memory_array_name,
            mem_modules,
            'data_memory',
            'mem'
        )

        self._instructions_array_name = deduce_name(
            self._instructions_array_name,
            mem_modules,
            'instruction_memory',
            'ram'
        )

    def _get_instructions_file_path(self):
        return os.path.join(self._get_instructions_folder_path(), self._instructions_file_name)

    def _get_build_folder_path(self):
        return os.path.join(os.getcwd(), self._build_folder_path)

    def _get_instructions_folder_path(self):
        return os.path.join(os.getcwd(), self._instructions_folder_path)

    def _get_build_file_path(self):
        return os.path.join(self._get_build_folder_path(), self._build_file_name)

    def _init_instructions_folder(self):
        if not os.path.isdir(self._get_instructions_folder_path()):
            os.mkdir(self._get_instructions_folder_path())

    def _init_build_folder(self):
        if not os.path.isdir(self._get_build_folder_path()):
            os.mkdir(self._get_build_folder_path())

    def _compile_tests(self):
        self._deduce_array_names()
        subprocess.check_output(
            f'iverilog -o {self._get_build_file_path()} {self._iverilog_build_flags} -I {self._cpu_files_folder} -DMEM_ARR="{self._memory_array_name}" -DREG_ARR="{self._registers_array_name}" -DINSTR_ARR="{self._instructions_array_name}" -DSOURCE_FILE="\\"{self._instructions_folder_path}/{self._instructions_file_name}\\"" {self.test_path}'
        )

    def _write_instructions(self, instructions: [Instruction]):
        if len(instructions) >= self._max_instructions:
            print('WARNING: can\'t safely reserve a cell for a breakpoint!')
            instructions = instructions[:self._max_instructions - 1]
        lines = '\n'.join(map(lambda x: x.binary(), instructions))
        with open(self._get_instructions_file_path(), 'w') as f:
            f.write(lines)
            # breakpoint
            f.write('\n' + '0' * 32)

    def _decode_tests_output(self, out):
        memory, registers = [], []
        memory_reading, reg_reading = False, False
        out = out.decode(encoding='utf-8')
        lines = out.split(os.linesep)
        for line in lines:
            line = line.strip()
            if line == 'MEMORY_DUMP_BEGIN':
                memory_reading = True
            elif line == 'MEMORY_DUMP_END':
                memory_reading = False
            elif line == 'REG_DUMP_BEGIN':
                reg_reading = True
            elif line == 'REG_DUMP_END':
                reg_reading = False
            elif line == 'FINISH':
                break
            else:
                if memory_reading:
                    parts = list(filter(lambda x: len(x) > 0, line.split(' ')))
                    index, value = int(parts[0]), twos_comp(int(parts[1], 2), 32)
                    _expand_array(memory, index + 1)
                    memory[index] = value

                if reg_reading:
                    parts = list(filter(lambda x: len(x) > 0, line.split(' ')))
                    index, value = int(parts[0]), twos_comp(int(parts[1], 2), 32)
                    _expand_array(registers, index + 1)
                    registers[index] = value
        return registers, memory

    def close(self):
        shutil.rmtree(self._get_build_folder_path(), ignore_errors=True)
        shutil.rmtree(self._get_instructions_folder_path(), ignore_errors=True)

    def run(self, instructions: [Instruction], time_out=None):
        if time_out is None:
            time_out = 2 ** 42
        self._write_instructions(instructions)
        command = f'vvp {self._get_build_file_path()}'
        output = subprocess.check_output(command, timeout=time_out/1000)
        return self._decode_tests_output(output)
